#!/usr/bin/env python
# encoding: utf-8
"""
IceROM.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.
"""

import sys
import os

class ROM:
    def __init__(self,path,emulator):
        self.path = path
        self.emulator = emulator
