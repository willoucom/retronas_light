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

import ftplib
import json
import os
import shutil
import random
import string
import re

from zipfile import ZipFile

myrient_host = "ftp.myrient.erista.me"

# Stucture of folders/remote
# f = Local Folder
# s = Remote/Source Folder
# z = (Optionnal) Zipfile name (default to games)
# b = (Optionnal) Backup Zipfile (default to True)
# o = (Optionnal) Create a Zipfile for each alphabet letter
# { "f":"", "s":""},
sets = []

alphabet = [
    "#", "_BetaProto", "_Homebrew", "_Aftermarket",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
]


def main():

    if os.path.isfile('myrient.json'):
        config = json.load(open('myrient.json'))
    else:
        exit("config file myrient.json not found")
    # Check config for rompath
    if "rompath" in config and config["rompath"]:
        RETRONAS_DIR = config["rompath"]
    else:
        exit("rompath not specified")
    # Check config for sets
    if "sets" in config and config["sets"]:
        sets = config["sets"]
    else:
        exit("sets not specified")

    # Main loop
    for set in sets:
        print(set["s"])
        zip_files = []
        # Zipfile name
        if not "z" in set:
            set["z"] = "games"

        # Check destination folder
        rompath = RETRONAS_DIR+set["f"]
        if not os.path.isdir(rompath):
            print(rompath+" not found, creating")
            os.makedirs(rompath, exist_ok=True)

        # Get local game list
        zip_files = getRomlist(rompath, set)
        # Write game list to disk
        file = open(rompath + '/gamelist.txt', 'w')
        for item in zip_files:
            file.write(item+"\n")
        file.close()

        # Connect FTP
        ftp = connectFTP(myrient_host)
        # Change ftp directory
        ftp.cwd(set["s"])
        # Get file list
        ftp_files = ftp.nlst()
        ftp.close()
        # Main loop
        for ftp_name in ftp_files:
            found = False
            for zip_name in zip_files:
                if os.path.splitext(ftp_name)[0] == os.path.splitext(zip_name)[0]:
                    found = True
                    zip_files.remove(zip_name)
                    break
            if not found:
                print(" " + ftp_name + " Not found, downloading")
                # Connect FTP
                ftp = connectFTP(myrient_host)
                ftp.cwd(set["s"])
                randomtempfile = "temp_" + \
                    "".join(random.choices(
                        string.ascii_lowercase, k=15)) + ".zip"
                # Download file
                try:
                    with open(randomtempfile, 'wb') as f:
                        ftp.retrbinary('RETR ' + ftp_name, f.write)
                        f.close()
                except ftplib.all_errors as e:
                    print(str(e))
                    ftp.close()
                    if os.path.isfile(randomtempfile):
                        os.remove(randomtempfile)
                    continue
                ftp.close()
                # Open file
                tmpzip = ZipFile(randomtempfile, "r")
                tmpzip_files = tmpzip.namelist()
                for tmp_name in tmpzip_files:
                    print("  Adding "+tmp_name)
                    if tmp_name in zip_files:
                        print(" > " + tmp_name + " already exists")
                        zip_files.remove(tmp_name)
                    else:
                        if not "o" in set or ("o" in set and set["o"] is False):
                            tmpfile = tmpzip.read(tmp_name)
                            zipfile = rompath+"/" + \
                                set["z"] + ".zip"
                            # Add file to games archive
                            addFileToZip(zipfile, tmpfile, tmp_name)
                        else:
                            # in case of split
                            # Get first letter
                            letter = destinationLetter(tmp_name)
                            zipfile = rompath+"/" + \
                                set["z"] + "_" + letter+".zip"
                            # Add file to games archive
                            createZip(zipfile)
                            tmpfile = tmpzip.read(tmp_name)
                            addFileToZip(zipfile, tmpfile, tmp_name)
                tmpzip.close()
                if os.path.isfile(randomtempfile):
                    os.remove(randomtempfile)

        # Cleaning zip
        # TODO: Rewrite zipfile
        for zip_name in zip_files:
            print(" " + zip_name)
        # Write leftovers to file
        file = open(rompath + '/leftovers.txt', 'w')
        for item in zip_files:
            file.write(item+"\n")
        file.close()
        print(set["s"] + " END")
        print("---")
    # Cleanup

    if os.path.isfile(rompath+"/"+set["z"]+"_backup.zip"):
        os.remove(rompath+"/"+set["z"]+"_backup.zip")

# Functions

def connectFTP(server):
    ftp = ftplib.FTP(myrient_host)
    ftp.login()
    return ftp


def createZip(name):
    # Check zip destination
    if not os.path.isfile(name):
        print(name + " not found, creating")
        with ZipFile(name, 'w') as file:
            pass


def backupZip(name):
    shutil.copy2(name, os.path.splitext(name)[0] + "_backup.zip")


def destinationLetter(name):
    # Get first letter
    letter = name[0]
    # Check in name
    if "(Homebrew)" in name:
        return "_Homebrew"
    if "(Beta)" in name or "(Proto)" in name or bool(re.search(r"\(Beta [0-9]+", name)) or bool(re.search(r"\(Proto [0-9]+", name)):
        return "_BetaProto"
    if "(Aftermarket)" in name or "(Unl)" in name:
        return "_Aftermarket"
    if letter in alphabet:
        return letter
    else:
        return "#"


def addFileToZip(zipfile: str, content: bytes, name: str):
    # Add file to games archive
    zip = ZipFile(zipfile, "a")
    zip.writestr(name, content)
    zip.close()


def getRomlist(rompath, set):
    zip_files = []
    # Option to split files
    if not "o" in set or ("o" in set and set["o"] is False):
        zipfile = rompath+"/"+set["z"]+".zip"
        createZip(zipfile)
        # Open Zip
        zip = ZipFile(zipfile, "r")
        zip_files = zip.namelist()
        zip.close()
    else:
        # If Split
        for letter in alphabet:
            zipfile = rompath+"/"+set["z"] + "_" + letter+".zip"
            # Open Zip
            if os.path.isfile(zipfile):
                zip = ZipFile(zipfile, "r")
                zip_files += zip.namelist()
                zip.close()
    return zip_files


main()
