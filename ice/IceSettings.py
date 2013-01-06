#!/usr/bin/env python
# encoding: utf-8
"""
IceSettings.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.

Basic settings to be used by the app.
"""

import sys
import os

appname = "Ice"
appdescription = "ROM Manager for Steam"
appauthor = "Scott Rice"

def platform_string():
    if sys.platform.startswith('win'):
        return "Windows"
    elif sys.platform.startswith('darwin'):
        return "OSX"
    else:
        return "Linux"