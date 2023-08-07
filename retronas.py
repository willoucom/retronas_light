#!/usr/bin/env python3

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Copyright 2023 Wilfried "willoucom" JEANNIARD

# You can download the latest version of this script from:
# https://github.com/willoucom/Retronas

import json
import os


# CREATE
folders = {}

def main():
    os.chdir(os.path.dirname(__file__))
    cmdlist = ["#!/bin/bash", "set -x"]
    lnlist = ["#!/bin/bash", "set -x"]
    fstab = ["# Retronas"]
    # Check for config
    if os.path.isfile('retronas.json'):
        config = json.load(open('retronas.json'))
    else:
        exit("missing config file")

    # Check for roms folder in config
    if "roms_folder" in config and config["roms_folder"]:
        retronas_roms = os.path.normpath(config["roms_folder"])
    else:
        exit("invalid config file")
    # Check for folders in config
    if "folders" in config and config["folders"]:
        folders = config["folders"]
    else:
        exit("invalid config file")
    # Check for mister folder in config
    if "mister_folder" in config and config["mister_folder"]:
        retronas_mister = os.path.normpath(config["mister_folder"])
    # Check for retroarch folder in config
    if "retroarch_folder" in config and config["retroarch_folder"]:
        retronas_retroarch = os.path.normpath(config["retroarch_folder"])

    # Check destination folder
    if "retronas_mister" in locals() and not os.path.isdir(retronas_mister):
        print(retronas_mister+" not found, creating")
        os.makedirs(retronas_mister, exist_ok=True)
    # Check destination folder
    if "retronas_retroarch" in locals() and not os.path.isdir(retronas_roms):
        print(retronas_roms+" not found, creating")
        os.makedirs(retronas_roms, exist_ok=True)

    for roms, options in folders.items():
        print("" + roms)
        # Check Roms folder
        rom_folder = os.path.normpath(retronas_roms + "/" + roms)
        checkFolder(rom_folder)
        # Check Mister folder
        if "retronas_mister" in locals() and 'Mister' in options:
            folders = options['Mister'].split(",")
            for f in folders:
                print(" M+ " + f)
                dest_folder = os.path.normpath(retronas_mister + "/" + f)
                # checkFolder(dest_folder)
                # Generate hardlink command
                lnlist += generateHardLinks(rom_folder, dest_folder)
                # Generate mount command
                cmdlist += generateMount(rom_folder, dest_folder)
                # Generate FSTAB
                fstab += generateFstab(rom_folder, dest_folder)
        # Check Retroarch folder
        if "retronas_retroarch" in locals() and 'Retroarch' in options:
            folders = options['Retroarch'].split(",")
            for f in folders:
                print(" R+ " + f)
                dest_folder = os.path.normpath(retronas_retroarch + "/" + f)
                # checkFolder(dest_folder)
                # Generate hardlink command
                lnlist += generateHardLinks(rom_folder, dest_folder)
                # Generate mount command
                cmdlist += generateMount(rom_folder, dest_folder)
                # Generate FSTAB
                fstab += generateFstab(rom_folder, dest_folder)

    file = open('retronas_mount.sh', 'w')
    if config['link_type'] == "symlinks":
    # Write lnlist to shell script
        for item in lnlist:
            file.write(item+"\n")
    if config['link_type'] == "bindmounts":
    # Write cmdlist to shell script
        for item in cmdlist:
            file.write(item+"\n")
    # Write fstab
    if config['link_type'] == "fstab":
        for item in fstab:
            file.write(item+"\n")
    file.close()

def generateMount(org, dest):
    cmd = []
    # Umount if already exists
    cmd.append("umount \"" + dest + "\"")
    # Mount bind
    cmd.append("mount --bind \"" + org + "\" \"" + dest + "\"")
    return cmd

def generateHardLinks(org, dest):
    cmd = []
    # 
    cmd.append("rm -fr \""+ dest +"\"")
    # SoftLink
    cmd.append("ln -s \"" + org + "/\" \"" + dest + "\"")
    return cmd

def generateFstab(org, dest):
    cmd = []
    cmd.append("" + org + " " + dest + " none defaults,bind 0 0")
    return cmd


def checkFolder(folder):
    if not os.path.isdir(folder):
        print(folder+" not found, creating")
        os.makedirs(folder, exist_ok=True)


main()
