# Retronas scripts collection


## Retronas


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
