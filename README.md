# Retronas scripts collection

Collection of scripts to help creating a NAS to store roms collection.

Legal notice : 
Depending on local legislation, it may be legal and/or illegal to store roms and iso files. Check with your local lawyer before using these scripts.

## Retronas

Create folders to store roms and iso files 

### Configuration

Edit `retronas.json`

Options:
```json
"roms_folder": "debug/roms/",
"mister_folder": "debug/retronas/mister/",
"retroarch_folder": "debug/retronas/retroarch/",
"link_type": "symlinks",
"folders": {}
```
+ roms_folder = location of your rom storage
+ mister_folder = location of the virtual storage for the MisterFPGA
+ retroarch_folder = location of the virtual storage for Retroarch
+ link_type = 
  + symlinks = use symbolic links
  + bindmounts = use mount --bind
  + fstab = create fstab file using mount --bind (may not work)

Folders section:
```json
"console/atari/atari2600": {
    "Mister": "Atari2600",
    "Retroarch": "atari2600"
},
```
+ Mister = name of the mister folder
+ Retroarch = name of the retroarch folder

### Usage

run `./retronas.py`

Generate folders and files depending on the options

### TODOs

+ Missing lot of systems for both the MisterFPGA and Retroarch
+ Fstab is not tested enough and may not work

List of missing systems for MisterFPGA:

EpochGalaxyII
Galaksija
Gamate
Homelab
Intellivision
Interact
Jupiter
Laser
Lynx48
MACPLUS
MegaDuck
MEMTEST
MISTER_saves
MultiComp
MyVision
ODYSSEY2
Ondra_SPO186
ORAO
Oric
PC8801
PCXT
PDP1
PET2001
PMD85
PocketChallengeV2
QL
RX78
SAMCOUPE
SharpMZ
Sord M5
Spectrum
SPMX
SuperVision
SuperVision8000
SVI328
Tamagotchi
TatungEinstein
TGFX16
TGFX16-CD
TI-99_4A
TomyScramble
TomyTutor
TRS-80
TSConf
UK101
VC4000
VECTOR06
VECTREX
VIC20
zx48
ZX81
ZXNext

## Myrient

Manage/Download/Update romsets from [Myrient](https://myrient.erista.me/)

Also can sort beta/unlicenced/homebrews to different zip files

### Configuration

Create a `myrient.json`

```json
{
    "rompath": "/data/retronas/roms/",
    "sets" : [
        { "f":"atari/2600", "s":"/No-Intro/Atari - 2600/", "o": "True", "z": "2600", "b": "False"},
        { "f":"atari/2600", "s":"/No-Intro/Atari - 2600/"}
    ]
}
```

+ f = the destination folder on your disk
+ s = the folder name on myrient
+ z = (Optionnal) Zipfile name (default to games)
+ b = (Optionnal) Backup Zipfile (default to True)
+ o = (Optionnal) Create a Zipfile for each alphabet letter and sort beta/unlicenced/homebrew

### Usage

run `./myrient.py` 

Generate some additionnal files on each folder : 

+ `gamelist.txt` contains list of present roms
+ `leftovers.txt` contains list of roms presents locally but not on Myrient
