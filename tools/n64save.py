#!/usr/bin/env python3
"""n64save: convert N64 save files between flashcart, FPGA and emulator formats.

Standard library only, except `wii-vc`, which needs the `cryptography` package.

Commands
  info FILE                      Identify a save file; list Controller Pak notes.
  convert IN OUT --type T [--from F] [--to F]
                                 Convert a cartridge save between byte orders.
                                 T: eep4k | eep16k | sram | flash
                                 F: native (SummerCart64, MiSTer, EverDrive, Wii VC) | pj64
  dex-cart IN OUT --type T [--note N]
                                 Pull a cartridge-EEPROM backup note (code 3BADD1E5,
                                 publisher FADE) out of a DexDrive .n64 file.
  dex-pak IN OUT --code GAME [--region R]
                                 Build a clean 32 KB Controller Pak image holding only the
                                 notes for one game (e.g. NKIE). --region relabels the
                                 last letter of the game code (e.g. P -> E). Output works as
                                 A3D controller_pak.img, MiSTer _1.cpk, Project64 .mpk and
                                 EverDrive .mpk.
  ids ROM                        Print the ROM's A3D cart ID, game code, CRC32, SHA1 and
                                 the save name Project64 will use.
  wii-vc DATA.BIN OUTDIR --dolphin DIR
                                 Decrypt a Wii Virtual Console data.bin and extract its files.
                                 Keys are read from a Dolphin source checkout (DIR), not stored here.
                                 EEP_xxxx / RAM_xxxx files inside are already in native order.

Byte order notes
  native = big-endian, as the cartridge stores it. SummerCart64 (.sav), MiSTer
  (.eep/.sra/.fla), EverDrive and Wii VC all use it.
  Project64 stores .sra and .fla as 32-bit little-endian words (every 4 bytes reversed);
  .eep and .mpk are native. Project64 may also write short files; we pad with 0xFF.
"""
import argparse
import hashlib
import os
import re
import struct
import sys
import zlib

SIZES = {'eep4k': 512, 'eep16k': 2048, 'sram': 32768, 'flash': 131072}
SWAPPED_IN_PJ64 = {'sram', 'flash'}


def swap32(b):
    b = b + b'\xff' * (-len(b) % 4)
    return b''.join(b[i:i + 4][::-1] for i in range(0, len(b), 4))


def fit(b, size):
    if len(b) > size:
        sys.exit(f'input is {len(b)} bytes, larger than the {size}-byte save type')
    return b + b'\xff' * (size - len(b))


# ---------------------------------------------------------------- Controller Pak

def pak_raw(data):
    """Return the 32 KB mempak inside a DexDrive file, or the data itself."""
    return data[0x1040:] if data[:11] == b'123-456-STD' else data


def dex_comments(data):
    if data[:11] != b'123-456-STD':
        return [''] * 16
    return [data[0x40 + i * 0x100:0x140 + i * 0x100].split(b'\0')[0].decode('latin1', 'replace') for i in range(16)]


def chain(mp, start):
    inode = mp[0x100:0x200]
    pages, p = [], start
    while 5 <= p < 128 and p not in pages:
        pages.append(p)
        nxt = int.from_bytes(inode[p * 2:p * 2 + 2], 'big')
        if nxt == 1:
            return pages
        p = nxt
    return None


def notes(mp):
    out = []
    for i in range(16):
        e = mp[0x300 + i * 32:0x320 + i * 32]
        start = int.from_bytes(e[6:8], 'big')
        if len(e) < 32 or e[:4] == b'\0\0\0\0' or not 5 <= start < 128:
            continue
        pages = chain(mp, start)
        data = b''.join(mp[q * 256:(q + 1) * 256] for q in pages) if pages else None
        out.append(dict(index=i, entry=e, code=e[:4].decode('latin1'), pub=e[4:6].decode('latin1'),
                        pages=pages, data=data))
    return out


_FONT = {0: '', 15: ' ', **{16 + i: str(i) for i in range(10)}, **{26 + i: chr(65 + i) for i in range(26)},
         52: '!', 53: '"', 54: '#', 55: "'", 56: '*', 57: '+', 58: ',', 59: '-', 60: '.', 61: '/', 62: ':',
         63: '=', 64: '?', 65: '@'}


def note_name(e):
    n = ''.join(_FONT.get(x, '~') for x in e[16:32]).rstrip()
    x = ''.join(_FONT.get(x, '~') for x in e[12:16]).rstrip()
    return n + ('.' + x if x else '')


# ID block of a real, valid Controller Pak (serial area zeroed), used for rebuilt paks.
_ID = bytes.fromhex('00080000ff010fe502baf6a600000000000000000000000000010100094ff6a3')


def id_ok(mp):
    for off in (0x20, 0x60, 0x80, 0xC0):
        b = mp[off:off + 32]
        s = sum(struct.unpack('>14H', b[:28])) & 0xFFFF
        c1, c2 = struct.unpack('>HH', b[28:32])
        if c1 == s and c2 == (0xFFF2 - s) & 0xFFFF:
            return True
    return False


def build_pak(entries):
    """entries: list of (32-byte note entry, data). Returns a formatted 32 KB pak."""
    pak = bytearray(0x8000)
    for off in (0x20, 0x60, 0x80, 0xC0):
        pak[off:off + 32] = _ID
    inode = bytearray(256)
    for p in range(5, 128):
        inode[p * 2:p * 2 + 2] = b'\x00\x03'
    table = bytearray(512)
    nxt = 5
    for k, (entry, data) in enumerate(entries):
        npg = (len(data) + 255) // 256
        if nxt + npg > 128:
            sys.exit('notes do not fit in one Controller Pak')
        pages = list(range(nxt, nxt + npg))
        for j, p in enumerate(pages):
            inode[p * 2:p * 2 + 2] = (pages[j + 1] if j + 1 < npg else 1).to_bytes(2, 'big')
            pak[p * 256:(p + 1) * 256] = data[j * 256:(j + 1) * 256].ljust(256, b'\0')
        e = bytearray(entry)
        e[6:8] = pages[0].to_bytes(2, 'big')
        e[8] |= 0x02
        table[k * 32:(k + 1) * 32] = e
        nxt += npg
    inode[1] = sum(inode[2:256]) & 0xFF
    pak[0x100:0x200] = inode
    pak[0x200:0x300] = inode
    pak[0x300:0x500] = table
    return bytes(pak)


# ---------------------------------------------------------------- ROM helpers

def rom_load(path):
    d = open(path, 'rb').read()
    if d[:4] == b'\x37\x80\x40\x12':  # .v64 byte-swapped
        d = b''.join(d[i:i + 2][::-1] for i in range(0, len(d), 2))
    elif d[:4] == b'\x40\x12\x37\x80':  # .n64 little-endian
        d = swap32(d)
    return d


def pj64_name(h):
    n = bytearray(h[0x20:0x34])
    i = 19
    while i >= 0 and n[i] in (0x20, 0):
        n[i] = 0
        i -= 1
    s = bytes(n).split(b'\0')[0].decode('latin1')
    return s.replace('/', '-').replace('\\', '-').replace(':', ';')


# ---------------------------------------------------------------- commands

def cmd_info(a):
    d = open(a.file, 'rb').read()
    if d[:11] == b'123-456-STD' or len(d) == 0x8000:
        mp = pak_raw(d)
        kind = 'DexDrive file' if d[:3] == b'123' else '32 KB Controller Pak image'
        print(f'{kind}; ID block {"valid" if id_ok(mp) else "missing/invalid"}')
        cm = dex_comments(d)
        for n in notes(mp):
            pg = len(n['pages']) if n['pages'] else 'BROKEN'
            tag = '  <- cartridge EEPROM backup' if n['code'] == ';\xad\xd1\xe5' or n['entry'][:4] == b'\x3b\xad\xd1\xe5' else ''
            print(f"note {n['index']:2}: {n['entry'][:4].hex()} {n['code']!r:8} pub {n['pub']!r:6} "
                  f"{note_name(n['entry'])!r:22} pages {pg}{tag}  {cm[n['index']]}")
        return
    guess = {512: 'eep4k', 2048: 'eep16k', 32768: 'sram', 131072: 'flash'}.get(len(d), '?')
    print(f'{len(d)} bytes; looks like {guess}. Byte order cannot be told from size alone; '
          'check for readable game strings in each order.')


def cmd_convert(a):
    d = open(a.inp, 'rb').read()
    size = SIZES[a.type]
    if a.frm == 'pj64' and a.type in SWAPPED_IN_PJ64:
        d = swap32(d)
    d = fit(d, size)
    if a.to == 'pj64' and a.type in SWAPPED_IN_PJ64:
        d = swap32(d)
    open(a.out, 'wb').write(d)
    print(f'wrote {a.out} ({len(d)} bytes)')


def cmd_dex_cart(a):
    d = open(a.inp, 'rb').read()
    found = [n for n in notes(pak_raw(d)) if n['entry'][:6] == b'\x3b\xad\xd1\xe5FA' or n['entry'][:4] == b'\x3b\xad\xd1\xe5']
    if a.note is not None:
        found = [n for n in found if n['index'] == a.note]
    if not found:
        sys.exit('no cartridge-EEPROM backup note (3BADD1E5) found; this is probably a game\'s own Controller Pak save')
    if len(found) > 1:
        sys.exit('several backup notes found, pick one with --note: ' + ', '.join(str(n['index']) for n in found))
    out = fit(found[0]['data'][:SIZES[a.type]], SIZES[a.type])
    open(a.out, 'wb').write(out)
    print(f'wrote {a.out} ({len(out)} bytes, native order)')


def cmd_dex_pak(a):
    mp = pak_raw(open(a.inp, 'rb').read())
    want = a.code.upper()
    picked = []
    for n in notes(mp):
        if n['code'][1:3] != want[1:3] or not n['pages']:
            continue
        e = bytearray(n['entry'])
        if a.region:
            e[3] = ord(a.region.upper())
        picked.append((bytes(e), n['data']))
    if not picked:
        sys.exit(f'no notes for {want} in this file')
    pak = build_pak(picked)
    open(a.out, 'wb').write(pak)
    print(f'wrote {a.out} with {len(picked)} note(s)')


def cmd_ids(a):
    d = rom_load(a.rom)
    print('a3d_cart_id ', '%08x' % zlib.crc32(d[:8192]))
    print('game_code   ', d[0x3b:0x3f].decode('latin1'), 'v%d' % d[0x3f])
    print('crc32       ', '%08x' % zlib.crc32(open(a.rom, 'rb').read()))
    print('sha1        ', hashlib.sha1(open(a.rom, 'rb').read()).hexdigest())
    print('pj64_name   ', repr(pj64_name(d)))


def cmd_wii_vc(a):
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    core = os.path.join(a.dolphin, 'Source', 'Core', 'Core')

    def arr(path, marker):
        s = open(path).read()
        seg = s[s.index(marker):][:800]
        vals = [int(x, 16) for x in re.findall(r'0x([0-9A-Fa-f]{2})\b', seg)][:16]
        assert len(vals) == 16, marker
        return bytes(vals)
    key = arr(os.path.join(core, 'IOS', 'IOSC.cpp'), 'm_key_entries[HANDLE_SD_KEY]')
    iv0 = arr(os.path.join(core, 'HW', 'WiiSave.cpp'), 's_sd_initial_iv{')

    def dec(b, iv):
        c = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
        return c.update(b) + c.finalize()
    b = open(a.inp, 'rb').read()
    hdr = dec(b[:0xF0C0], iv0)
    print('title id', hdr[4:8].decode('latin1'))
    nfiles = struct.unpack('>I', b[0xF0C0 + 12:0xF0C0 + 16])[0]
    pos = 0xF0C0 + 0x80
    os.makedirs(a.outdir, exist_ok=True)
    for _ in range(nfiles):
        fh = b[pos:pos + 0x80]
        pos += 0x80
        magic, size = struct.unpack('>II', fh[:8])
        typ = fh[10]
        name = fh[11:0x4B].split(b'\0')[0].decode('latin1')
        if magic != 0x03ADF17E:
            sys.exit('unexpected file header')
        if typ == 1:
            r = (size + 63) // 64 * 64
            data = dec(b[pos:pos + r], fh[0x50:0x60])[:size]
            pos += r
            out = os.path.join(a.outdir, name.replace('/', '__'))
            open(out, 'wb').write(data)
            print(f'{name}  {size} bytes')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest='cmd', required=True)
    x = s.add_parser('info'); x.add_argument('file'); x.set_defaults(f=cmd_info)
    x = s.add_parser('convert'); x.add_argument('inp'); x.add_argument('out')
    x.add_argument('--type', required=True, choices=SIZES)
    x.add_argument('--from', dest='frm', default='native', choices=['native', 'pj64'])
    x.add_argument('--to', default='native', choices=['native', 'pj64']); x.set_defaults(f=cmd_convert)
    x = s.add_parser('dex-cart'); x.add_argument('inp'); x.add_argument('out')
    x.add_argument('--type', required=True, choices=['eep4k', 'eep16k']); x.add_argument('--note', type=int)
    x.set_defaults(f=cmd_dex_cart)
    x = s.add_parser('dex-pak'); x.add_argument('inp'); x.add_argument('out')
    x.add_argument('--code', required=True); x.add_argument('--region'); x.set_defaults(f=cmd_dex_pak)
    x = s.add_parser('ids'); x.add_argument('rom'); x.set_defaults(f=cmd_ids)
    x = s.add_parser('wii-vc'); x.add_argument('inp'); x.add_argument('outdir')
    x.add_argument('--dolphin', required=True); x.set_defaults(f=cmd_wii_vc)
    a = p.parse_args()
    a.f(a)


if __name__ == '__main__':
    main()
