# N64 Game Saves

Unlocked or near-complete save files for Nintendo 64 games, converted for the
SummerCart64, ModRetro M64, MiSTer, Analogue 3D, Project64, and EverDrive.

- **55 cartridge saves** (EEPROM, SRAM, FlashRAM): 37 ready, 17 need review, 1 revision mismatch
- **92 Controller Pak saves**: 49 ready, 43 need review

Every save was collected from a public source and credited in [CREDITS.md](CREDITS.md).
No ROMs are included.

## Contents

| Folder | What's in it |
|---|---|
| `saves/summercart64/` | Cartridge saves as `<ROM name>.sav` |
| `saves/mister/` | Cartridge saves (`.eep` `.sra` `.fla`) and Controller Pak saves (`<ROM name>_1.cpk`) |
| `saves/analogue3d/` | Controller Pak saves as an Analogue 3D `Library/N64/Games` tree |
| `saves/emulator/` | Project64 format: cartridge saves and Controller Paks (`_Cont_1.mpk`) |
| `saves/controller-pak/` | Controller Pak images as `<ROM name>.mpk` (raw 32 KB), for writing to a real Controller Pak |
| `saves/everdrive/` | Cartridge saves as `<ROM name>.srm` `.eep` `.fla`. **Untested**, see below |
| `originals/` | Every save exactly as downloaded, in its original format |
| `data/games.csv` | One row per ROM in the set these were built against (343 No-Intro 1G1R ROMs, mostly USA): CRC32, SHA1, save type, status, source, file paths |
| `data/credits.csv` | Creator, source link, stated completion and redistribution notes for every save |
| `tools/n64save.py` | The conversion tool used to build all of the above |

The [Releases](../../releases) page has one zip per device if you only want one set.

## Match your ROM first

Saves are named after No-Intro 1G1R ROM file names (USA where one exists). Look up your ROM in
`data/games.csv` by CRC32 or SHA1. If the hash matches but your file name differs,
rename the save to match your ROM's file name. If the hash doesn't match, you
have a different revision or region and the save may not work.

`python3 tools/n64save.py ids <rom>` prints a ROM's hashes, game code, Analogue 3D
cart ID and Project64 save name.

## Install

### SummerCart64 (N64FlashcartMenu)

Copy the `.sav` files into the `saves` folder that sits next to your ROMs
(the menu's default). Tested on an original N64 and an Analogue 3D with GoldenEye 007,
Super Smash Bros., Paper Mario, F-Zero X and Pokemon Stadium.

The SummerCart64 can't emulate a Controller Pak, but N64FlashcartMenu 0.3.4 and later
can write one of the `saves/controller-pak/` files onto a real Controller Pak: with the
Pak in a controller, browse to the `.mpk` file in the menu and restore it. This
overwrites everything on the Pak, so back it up first from the menu's Controller Pak
manager (press Start). On an Analogue 3D, use its virtual Controller Pak instead
(see below).

### ModRetro M64

Cartridge saves work through your flashcart: the M64 runs the SummerCart64 and the
EverDrive X5/X7, so use the files for your cart. Not tested on an M64 yet.

The M64 has no virtual Controller Pak yet (it's on ModRetro's update roadmap), so Pak saves
go on a real Controller Pak, written with the SummerCart64 menu as described above or with
an EverDrive.

### MiSTer

Copy everything in `saves/mister/` to `/media/fat/saves/N64/`. Cartridge saves load
automatically. `_1.cpk` files are player 1's Controller Pak; enable the Controller Pak in
the core's menu.

### Analogue 3D

Copy the `Library` folder from `saves/analogue3d/` to the root of the A3D's SD card,
merging with the `Library` folder already there. Each game folder is matched by the
8-digit ID at the end of its name (the CRC32 of the first 8 KB of the ROM). The game
won't show up in the A3D library until you boot it once, but when you do, it loads the
Pak from its folder. Back up any existing `controller_pak.img` you want to keep before
overwriting it. Turn on the virtual Controller Pak for the game.

Cartridge saves on the A3D come from your flashcart (use the SummerCart64 files).

### Project64

Copy `saves/emulator/` into Project64's `Save` folder. Project64 names saves after the
title in the ROM header, not the file name (`GOLDENEYE.eep`, `TWINE_Cont_1.mpk`).
SRAM and FlashRAM files are stored in Project64's byte order. Choro Q 64 2 and
Virtual Pro Wrestling 2 have Japanese header titles, so their files are named after
the ROM; rename them to whatever Project64 creates.

### EverDrive 64 (untested)

The save data is the same as the SummerCart64 files (the byte order was checked against
an EverDrive pack), only renamed: `.srm` for SRAM, `.eep`, `.fla`. Community docs put
saves in `ED64/gamedata`; Krikzz's X7 manual says `ED64/save`. EverDrives don't emulate
the Controller Pak, but the `saves/controller-pak/` files can be written to a real Pak
from the EverDrive file menu. If you have an EverDrive, please open an issue with what works.

## Status

- **ready**: source states a full or near-full unlock, matching region and revision.
- **needs review**: something to check before trusting it. Completion not stated, partial
  progress, a European save relabeled for the USA game, a Japanese save on an English
  patch, or a byte order that had to be inferred. The reason is in `data/games.csv`.
- **revision mismatch**: made for a different ROM revision than the one listed. Test first.

## Games

| Game | Save | Status | Completion (source's description) |
|---|---|---|---|
| 007 - The World Is Not Enough | Controller Pak | ready | Everything done and unlocked |
| 1080° Snowboarding | Cartridge (SRAM 256Kbit) | needs review | Not stated per file. Repo README: saves focused on multiplayer content and unlockables (levels, characters, b… |
| Aidyn Chronicles - The First Mage | Controller Pak | needs review | Save files near the end of the game. One before the final battle, and one on the way to Erromon. |
| All-Star Baseball 99 | Controller Pak | needs review | This contains T64's all-star roster for the Pirates. It has all the big named players. |
| Animal Forest | Controller Pak | needs review | Original Controller Pak Data - 2 Famicom Games and 1 Song at Post Office |
| Army Men - Sarge's Heroes 2 | Controller Pak | needs review | Starts you at the final save point in the game |
| Automobili Lamborghini | Controller Pak | ready | All cars and reverse modes unlocked by T64. |
| Banjo-Kazooie | Cartridge (EEPROM 4Kbit) | ready | Game fully completed with everything unlocked by T64. |
| Banjo-Tooie | Cartridge (EEPROM 16Kbit) | ready | All 90 jiggies and 900 notes collected, all 25 honey combs, all 45 jinjos, all 25 cheat pages collected with… |
| BattleTanx | Controller Pak | needs review | T64's save with extra options available! |
| BattleTanx - Global Assault | Controller Pak | needs review | Starts you at final save point with a lot of tank bucks |
| Beetle Adventure Racing! | Controller Pak | ready | The fully unlocked T64 save file. |
| Bio F.R.E.A.K.S | Controller Pak | needs review | Start at Mutilator with Bullzeye by T64. |
| Blast Corps | Controller Pak | ready | T64 fully unlocked save file. |
| Bomberman 64 | Cartridge (EEPROM 4Kbit) | ready | File 1: Hard Mode, game cleared with all Gold Cards and Costume Pieces obtained. File 2: Normal Mode, game cl… |
| Bomberman 64: The Second Attack! | Cartridge (EEPROM 4Kbit) | needs review | Not stated per file. Repo README: saves focused on multiplayer content and unlockables. |
| Bomberman Hero | Cartridge (EEPROM 4Kbit) | ready | NA3E - 100% completion with all mini-game modes unlocked |
| Buck Bumble | Controller Pak | needs review | Saves at levels 12-19, 9 lives for final level |
| Bust-A-Move '99 | Controller Pak | ready | T64Mike's completed Bust-A-Move '99 save. Puzzles unlocked. |
| California Speed | Controller Pak | ready | All cars and tracks unlocked. |
| Castlevania | Controller Pak | needs review | T64 at final area with two characters to kill Dracula. |
| Castlevania - Legacy of Darkness | Controller Pak | ready | 100%, All Characters, All Costumes, Hard Mode Unlocked |
| Chameleon Twist 2 | Controller Pak | ready | All four characters with everything unlocked, T64. |
| Choro Q 64 2 - Hacha Mecha Grand Prix Race | Controller Pak | needs review | Every Part and unlockable item saved |
| Conker's Bad Fur Day | Cartridge (EEPROM 16Kbit) | needs review | 100% done \| In-file DexDrive comment: "Game Completed" |
| Cruis'n USA | Cartridge (EEPROM 4Kbit) | ready | NASE - All upgrades unlocked (including those for secret vehicles) |
| CyberTiger | Controller Pak | ready | All bonus costumes, characters and hidden volcano course unlocked. |
| Deadly Arts | Controller Pak | ready | All of the characters unlocked, T64. |
| Destruction Derby 64 | Controller Pak | ready | Has all tracks, cars and even some killer times and scores to beat! |
| Diddy Kong Racing | Cartridge (EEPROM 4Kbit) | ready | All ballons adventure 1, all ballons in adventure 2, and Drumstick and T.T. are unlocked as playable characte… |
| Donald Duck - Goin' Quackers | Controller Pak | needs review | Not stated |
| Donkey Kong 64 | Cartridge (EEPROM 16Kbit) | ready | 101% completion with all 201 golden bananas, all 100 regular bananas for every kong in each world, all banana… |
| Doom 64 | Controller Pak | needs review | Saves for most levels |
| Dr. Mario 64 | Cartridge (EEPROM 4Kbit) | needs review | Not stated per file. Repo README: saves focused on multiplayer content and unlockables (levels, characters, b… |
| Dual Heroes | Controller Pak | ready | Everything done |
| Duke Nukem - Zero Hour | Controller Pak | needs review | First two parts for time machine collected |
| Duke Nukem 64 | Controller Pak | needs review | Level 23 on the hardest diffculty setting. |
| ECW Hardcore Revolution | Controller Pak | ready | All the hidden wrestlers and cheats unlocked. |
| Extreme-G | Controller Pak | ready | Both extra bikes and the extra track unlocked (100 % complete) |
| Extreme-G XG2 | Controller Pak | ready | Extra levels and characters unlocked. |
| F-Zero X | Cartridge (SRAM 256Kbit) | ready | All cups unlocked and complete, all vehicles and difficulties unlocked, all staff ghosts beaten, every single… |
| F1 Pole Position 64 | Controller Pak | ready | Game beaten and hold a & b buttons at loading screen to get a faster 96' forties car. |
| Fighter Destiny 2 | Cartridge (EEPROM 4Kbit) | needs review | Not stated per file. Repo README: saves focused on multiplayer content and unlockables. |
| Fighters Destiny | Cartridge (EEPROM 4Kbit) | needs review | Not stated per file. Repo README: saves focused on multiplayer content and unlockables (levels, characters, b… |
| Fighting Force 64 | Controller Pak | needs review | Starts you at the final save point in the game |
| Forsaken 64 | Controller Pak | ready | Everything unlocked |
| Gauntlet Legends | Controller Pak | needs review | Two game saves, Koric and Lori. On the last level with very high levels on each. |
| Gex 64 - Enter the Gecko | Controller Pak | needs review | All remotes, all levels available |
| Goemon's Great Adventure | Controller Pak | ready | The game is 100% completed. All 44 passes obtained. All 12 alternative costumes unlocked. 99 Lives. 999 coins. |
| GoldenEye 007 | Cartridge (EEPROM 4Kbit) | ready | All cheats and All levels completed \| In-file DexDrive comment: "All Cheats and game Completed" |
| Hercules - The Legendary Journeys | Controller Pak | needs review | Up to town San Tomanicus, ready to beat the third minotaur. |
| Hot Wheels - Turbo Racing | Controller Pak | ready | The T64 save with everything unlocked. |
| Hybrid Heaven | Controller Pak | needs review | Level 3.1, Normal Difficulty. |
| Hydro Thunder | Controller Pak | ready | All watercraft and levels unlocked |
| International Superstar Soccer '98 | Controller Pak | needs review | 6 All-star teams unlocked. For PAL version |
| International Superstar Soccer 2000 | Controller Pak | needs review | 6 All-stars teams unlocked. For PAL En/De version, just rename to .mpk |
| International Superstar Soccer 64 | Controller Pak | needs review | 6 All-star teams unlocks. For PAL version, just rename to .mpk |
| International Track & Field 2000 | Controller Pak | needs review | All 14 Gold Medals obtained, all 4 hidden events unlocked |
| Jet Force Gemini | Cartridge (FlashRAM 1Mbit) | needs review | Jet Force Gemini Almost 100% Main Menu Unlockables |
| Killer Instinct Gold | Controller Pak | ready | Everything Unlocked |
| Kirby 64 | Cartridge (EEPROM 4Kbit) | ready | NAME - All Crystal Shards, Boss Battles, All Mini Game Difficulties Unlocked! |
| LEGO Racers | Controller Pak | needs review | Not stated |
| Mario Golf | Cartridge (SRAM 256Kbit) | ready | NAUE - 100% Completed |
| Mario Kart 64 | Cartridge (EEPROM 4Kbit) | ready | 100% completed \| In-file DexDrive comment: "Everything Completed" |
| Mario Party | Cartridge (EEPROM 4Kbit) | ready | 100% clear \| In-file DexDrive comment: "All items bought. Game beaten." |
| Mario Party 2 | Cartridge (EEPROM 4Kbit) | ready | NAZE - 100% Complete, Bowser Land Unlocked & Cleared, Credits Machine Unlocked, 99,999 Coins, All Mini-Games… |
| Mario Party 3 | Cartridge (EEPROM 16Kbit) | needs review | Not stated per file. Repo README: saves focused on multiplayer content and unlockables (levels, characters, b… |
| Mario Tennis | Cartridge (EEPROM 16Kbit) | ready | NATE - Played from Pikachu025 file - Every Tournaments/Star Tournaments completed for all characters in Singl… |
| Mega Man 64 | Cartridge (FlashRAM 1Mbit) | ready | At Main Gate with all items & key items, special weapons upgraded to the max, side quests completed, and hard… |
| Mickey's Speedway USA | Cartridge (EEPROM 4Kbit) | ready | All Cups, Ludwig, Huey, & New Orleans unlocked. "Should have everything unlocked." |
| Mischief Makers | Cartridge (EEPROM 4Kbit) | ready | A 100% save file for v1.1 of Mischief Makers.All yellow gems, all S ranks, and maxed out red gems.I saw nobod… |
| Mission: Impossible | Cartridge (EEPROM 4Kbit) | ready | T64 M:I save with all missions completed, everything unlocked. \| In-file DexDrive comment: "Mission: Impossi… |
| Mortal Kombat 4 | Controller Pak | needs review | Not stated |
| Mystical Ninja Starring Goemon | Controller Pak | ready | All dolls found, Consecutive Boss Battle Mode unlocked, save points at end and before outer space |
| NASCAR 2000 | Controller Pak | ready | Championship finished in first place |
| NBA Hangtime | Controller Pak | needs review | Created player. Maxed out stats. All records set. |
| Nightmare Creatures | Controller Pak | ready | T64's game entirely unlocked. |
| Ogre Battle 64 - Person of Lordly Caliber | Controller Pak | needs review | Last scene, perfect chaos frame, tons of money and equipment, and powerful units. ALL hero classes, including… |
| Paper Mario | Cartridge (FlashRAM 1Mbit) | ready | The True 100% Save! Every Sidequest, Badge, Star Piece, Recipe, Quiz, Star Power, and other things collected!… |
| Penny Racers | Controller Pak | ready | All 114 parts saved |
| Perfect Dark | Cartridge (EEPROM 16Kbit) | needs review | Not stated per file. Repo README: saves focused on multiplayer content and unlockables (levels, characters, b… |
| Pilotwings 64 | Cartridge (EEPROM 4Kbit) | needs review | Not stated per file. Repo README: saves focused on multiplayer content and unlockables (levels, characters, b… |
| Pokémon Snap | Cartridge (FlashRAM 1Mbit) | ready | NAKE- 100% Completed |
| Pokémon Stadium | Cartridge (FlashRAM 1Mbit) | ready | Round 1 + 2 fully complete. stadium, gym leader's castle, and rival beaten. Hyper difficulty in the mini game… |
| Pokémon Stadium 2 | Cartridge (FlashRAM 1Mbit) | ready | Round 1 + 2 fully complete. Jotho and Kanto gym leaders complete, and rival beaten. Pokemon Academy complete,… |
| Polaris SnoCross | Controller Pak | ready | Every level and snow mobile are unlocked |
| Power Rangers - Lightspeed Rescue | Controller Pak | ready | All levels and multiplayer characters unlocked. Plus, if you press Z while you highlight a certain level, you… |
| Quake II | Controller Pak | needs review | This will take you to the last level. |
| Rampage - World Tour | Controller Pak | needs review | High levels available |
| Rayman 2 - The Great Escape | Controller Pak | ready | 100% complete, all lums, all cages, full energy, and at the last boss. |
| Re-Volt | Controller Pak | ready | Every car and track unlocked. Also includes a few custom track files. |
| Ready 2 Rumble Boxing - Round 2 | Controller Pak | ready | All boxers are unlocked |
| Resident Evil 2 | Cartridge (SRAM 256Kbit) | needs review | Hunk and Tofu modes unlocked, all infinite weapons unlocked for arranged mode, and saves for Claire A/B & Leo… |
| Road Rash 64 | Controller Pak | needs review | Not stated |
| Robotron 64 | Controller Pak | ready | Saves at lvl200(Easy), lvl200(Hard), and intervalic saves on Normal up to lvl200 |
| Rush 2 - Extreme Racing USA | Controller Pak | needs review | Not stated |
| San Francisco Rush - Extreme Racing | Controller Pak | ready | 100 % all done, everything unlocked |
| San Francisco Rush 2049 | Controller Pak | needs review | Circuit, stunt and obstacle modes completed, all coins, vehicles and parts. |
| Scooby-Doo! - Classic Creep Capers | Controller Pak | needs review | Saved just before the Ghoul King trap with lots of Courage. |
| Shadow Man | Controller Pak | ready | Everything completed |
| Shadowgate 64 - Trials of the Four Towers | Controller Pak | needs review | Just about to beat the game |
| Sin and Punishment (Tsumi to Batsu) | Cartridge (EEPROM 4Kbit) | needs review | EEPROM Save: Hard Game Level and all options in OPT. menu unlocked. |
| Snowboard Kids | Controller Pak | needs review | Not stated |
| Snowboard Kids 2 | Cartridge (EEPROM 4Kbit) | needs review | Not stated per file. Repo README: saves focused on multiplayer content and unlockables (levels, characters, b… |
| South Park | Controller Pak | needs review | Starts you at final save point in the game |
| South Park Rally | Controller Pak | needs review | Not stated |
| Space Invaders | Controller Pak | ready | Classic mode available, saved games at final boss of Expert, Normal, and Maniacal Mode (in that order) |
| Space Station Silicon Valley | Cartridge (EEPROM 4Kbit) | needs review | 100% Power Cells, and all Trophies except Fat Bear Mountain. |
| Spider-Man | Controller Pak | ready | 100% completed |
| Star Fox 64 | Cartridge (EEPROM 4Kbit) | ready | 100% completed \| In-file DexDrive comment: "EEPROM: All medals, expert and normal modes accessible, sound mo… |
| Star Soldier: Vanishing Earth | Cartridge (EEPROM 4Kbit) | needs review | Not stated per file. Repo README: saves focused on multiplayer content and unlockables. |
| Star Wars Episode I: Battle for Naboo | Cartridge (EEPROM 4Kbit) | ready | All levels with Platinum Medals. \| In-file DexDrive comment: "All Levels with Platinum Medals." |
| Star Wars Episode I: Racer | Cartridge (EEPROM 16Kbit) | ready | All tracks and pod-racers unlocked (including hidden characters Cy Yunga and Jinn Reeso), all tracks and mirr… |
| Star Wars: Shadows of the Empire | Cartridge (EEPROM 4Kbit) | needs review | EEPROM Save: All Challenge Points collected on both Medium and Jedi settings. |
| Super Mario 64 | Cartridge (EEPROM 4Kbit) | ready | Ultimate 100% save, all coin collected in all courses, 120 star, all cap switch opened, all area unlocked, ba… |
| Super Robot Spirits | Cartridge (EEPROM 4Kbit) | ready | All characters and costumes unlocked. \| In-file DexDrive comment: "Created with savefileconverter.com" |
| Super Smash Bros. | Cartridge (SRAM 256Kbit) | ready | NALE--all characters and multiplayer stages unlocked as well as the Sound Test and Item Switch options |
| Tarzan | Controller Pak | needs review | 100% played in heavy or hard game mode. Have fun! |
| The Legend of Zelda: Majora's Mask | Cartridge (FlashRAM 1Mbit) | ready | NARE - 100% Complete! 24 Masks, 6 Bottles, 20 hearts, All Items, All Songs, All Great Fairy Items! Fierce Dei… |
| The Legend of Zelda: Ocarina of Time | Cartridge (SRAM 256Kbit) | revision mismatch | File 1 - Name: Link, 100% Complete, All 100 Gold Skulltulas Defeated, All Heart Pieces Collected, All Items a… |
| The New Tetris | Cartridge (SRAM 256Kbit) | ready | 400k lines completed, all wonders except last one unlocked |
| Tom and Jerry in Fists of Furry | Cartridge (EEPROM 4Kbit) | ready | Every character is unlocked and every stage is unlocked |
| Tonic Trouble | Controller Pak | needs review | Groghs Kingdom can be reached |
| Tony Hawk's Pro Skater | Controller Pak | ready | All the skaters have full stats, 30 tapes, and 3 gold medals. Just load it up and have fun. |
| Tony Hawk's Pro Skater 2 | Controller Pak | needs review | Not stated |
| Tony Hawk's Pro Skater 3 | Controller Pak | needs review | Not stated |
| Toy Story 2 - Buzz Lightyear to the Rescue! | Controller Pak | ready | All levels unlocked and all 50 pizza planet tokens earned. |
| Turok - Dinosaur Hunter | Controller Pak | ready | ALL Keys, all chronoscepter pieces, all cheats, and starts you at the final save point in the game |
| Turok - Rage Wars | Controller Pak | ready | 48 medals, all mini-game icons, all cheats, all weapon upgrades and all extra game modes. |
| Turok 2 - Seeds of Evil | Controller Pak | ready | All keys, Talismans, and nuke pieces and starts you at final save point in the game |
| Turok 3 - Shadow of Oblivion | Controller Pak | needs review | Start at Final Boss with Joseph. |
| Vigilante 8 | Controller Pak | ready | Game Completely Beaten |
| Virtual Pro Wrestling 2 - Oudou Keishou | Controller Pak | needs review | Save file contains 16 full Created Wrestlers, (CAWs.) CAWs are of WWF wrestlers. |
| Wave Race 64 | Cartridge (EEPROM 4Kbit) | ready | All championship modes unlocked including reverse mode, Glacier Coast and Twilight City courses unlocked, and… |
| WCW Backstage Assault | Controller Pak | ready | All wrestlers, costumes, and moves unlocked |
| WCW Mayhem | Controller Pak | ready | All the hidden wrestlers unlocked. |
| WCW Nitro | Controller Pak | ready | All wrestlers with unfinished programmer and nitro girl wrestlers. |
| WCW vs. nWo - World Tour | Controller Pak | ready | Every title won and all the secret wrestlers unlocked |
| WCW/nWo Revenge | Cartridge (SRAM 256Kbit) | ready | A straight dump from my cart with all items unlocked. (Summercart64 versions marked tested.) |
| WinBack - Covert Operations | Controller Pak | ready | Sudden Death, Max Power, and Trial modes unlocked, All Hidden Characters unlocked and game beaten on easy, no… |
| Worms Armageddon | Cartridge (EEPROM 4Kbit) | needs review | Not stated per file. Repo README: saves focused on multiplayer content and unlockables. |
| WWF Attitude | Controller Pak | ready | All the hidden wrestlers and cheats unlocked. |
| WWF No Mercy | Cartridge (FlashRAM 1Mbit) | ready | All wrestlers unlocked and everything purchased from the SmackDown Mall. No CAWs. Confirmed to work in both r… |
| WWF War Zone | Controller Pak | ready | All the hidden wrestles and cheats unlocked. |
| WWF WrestleMania 2000 | Cartridge (SRAM 256Kbit) | ready | All Characters unlocked, inc. Ho & Dummy, Smokin' Skull AND Light Heavyweight Unlocked - converted from PJ64… |
| Xena - Warrior Princess - The Talisman of Fate | Controller Pak | ready | This is a save containing Despair as a playable character unlocked by T64. |
| Yoshi's Story | Cartridge (EEPROM 16Kbit) | ready | 100% Complete, black and white Yoshis unlocked for story mode, and all stages available for trial mode (100%) |

Games with no save found are listed in `data/games.csv` with status `not found`.

## Credits and licensing

The saves belong to the people who made them; see [CREDITS.md](CREDITS.md). No source
asked for its saves not to be reposted. If you made one of these saves and want it
credited differently or removed, open an issue.

The tools, documentation and data files are MIT licensed (see [LICENSE](LICENSE)).
That license does not cover the save files themselves.

## Adding a save

```
python3 tools/n64save.py info file.n64                       # what's inside a DexDrive file or pak
python3 tools/n64save.py dex-cart file.n64 out.sav --type eep4k   # cartridge EEPROM backup -> .sav
python3 tools/n64save.py dex-pak file.n64 out.img --code NKIE     # Controller Pak notes -> clean pak image
python3 tools/n64save.py convert in.sra out.sav --type sram --from pj64
```
