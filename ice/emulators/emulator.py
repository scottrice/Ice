#!/usr/bin/env python
# encoding: utf-8
"""
Emulator.py

Created by Scott on 2013-01-04.
Copyright (c) 2013 Scott Rice. All rights reserved.

Emulator is the base class of all my emulators.

Functionality should be added here if every single emulator (whether downloaded
or not) would use it
"""

import sys
import os
import urllib

import abc

class Emulator(object):
    __metaclass__ = abc.ABCMeta
    
    # Location should be set by any subclasses which manage where emulators
    # are stored (such as the Downloaded Emulator class)
    location = ""
    
    # Since one emulator may handle many consoles, it is important to make sure
    # we specify which console we are having the emulator handle currently
    def __init__(self,console_name):
        self._console_name_ = console_name
        
    def valid_rom(self,path):
        """
        This function determines if a given path is actually a valid ROM file.
        There are many different file extensions that could be used as ROMs,
        and it would be a pretty bad user experience if a valid rom got ignored
        by Ice, so I will err on the side of "Valid". The exception to this is
        bsnes, whose functionality should be described in it's class
        """
        return True
    
    @abc.abstractmethod
    def command_string(self):
        """
        Returns the string which is used by Steam to launch the Emulator+ROM
        """
        return
        
    def startdir(self,rom):
        """
        Returns the directory which stores the emulator. This value is useful
        as the 'StartDir' option of a Steam Shortcut
        """
        return os.path.dirname(self.location)