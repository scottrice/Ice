#!/usr/bin/env python
# encoding: utf-8
"""
config_error.py

Created by Scott on 2013-05-23.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os

class ConfigError(StandardError):
    def __init__(self, section, key, fix_instructions, file="config.txt"):
        self.section = section
        self.key = key
        self.fix_instructions = fix_instructions
        self.file = file
        
    def __str__(self):
        return repr("[%s] %s || %s" % (self.section, self.key, self.fix_instructions))