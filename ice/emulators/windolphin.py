#!/usr/bin/env python
# encoding: utf-8
"""
windolphin.py

Created by Scott on 2013-01-05.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os

import downloaded_emulator

class WinDolphin(downloaded_emulator.DownloadedEmulator):
    _download_location_ = "https://dl.dropbox.com/u/2862706/ice_emulators/WinDolphin.zip"
    _relative_exe_path_ = os.path.join("WinDolphin","Dolphin.exe")
    
    def __init__(self,console_name):
        super(WinDolphin,self).__init__(console_name)