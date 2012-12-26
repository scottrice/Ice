#!/usr/bin/env python
# encoding: utf-8
"""
IceConsole.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.
"""

import sys
import os

import IceFilesystemHelper

class Console():
    def __init__(self,shortname,fullname,emulator):
        self.shortname = shortname
        self.fullname = fullname
        self.emulator = emulator
        
    def path(self):
        return IceFilesystemHelper.path_for_console(self)
        
    def find_all_roms(self):
        return []

def find_all_roms():
    all_roms = []
    for console in supported_consoles:
        all_roms.extend(console.find_all_roms())
    return all_roms

# TODO: Emulator should be an object, not a string...
n64 = Console("N64","Nintendo 64","")

supported_consoles = [
    # nes,
    # snes,
    n64#,
    # ps1,
    # ps2,
    # genesis,
    # dreamcast,
    # gameboy,
    # gba,
    # ds
]