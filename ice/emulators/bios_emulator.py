#!/usr/bin/env python
# encoding: utf-8
"""
config_emulator.py

Created by Scott on 2013-01-24.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os
import abc
import shutil

import IceFilesystemHelper
from IceLogging import log

import emulator

class BiosEmulator(emulator.Emulator):
    __metaclass__ = abc.ABCMeta
    
    # Should be overwritten by a subclass
    #
    # Describes the relative path to the directory in which the bios should
    # be placed (once the user provides it)
    _bios_directory_ = None
    
    # Should be overwritten by a subclass
    #
    # The name of the BIOS. This should be used to help a user figure out
    # which BIOS to provide, along with telling Ice what to rename the BIOS
    # file once it is provided
    _bios_name_ = None
    
    def __init__(self,console_name):
        assert self._bios_directory_, "Bios Directory must be defined for all subclasses of BiosEmulator"
        assert self._bios_name_, "Bios Name must be defined for all subclasses of BiosEmulator"
        super(BiosEmulator,self).__init__(console_name)
        
    def __check_for_user_supplied_bios__(self):
        # If the bios already exists, we don't need to do anything
        if os.path.exists(self.emulator_bios_location()):
            log("Found bios in emulator already")
            return
        if os.path.exists(user_supplied_bios_location()):
            # The user has given us a bios, we should copy the file to the 
            # correct location
            log("Found bios in ROMs directory, copying it to emulator location")
            shutil.copyfile(self.user_supplied_bios_location(),self.emulator_bios_location())
            return
        log("No bios found")
        
    def is_functional(self):
        """
        This emulator is only functional if the user has provided a BIOS.
        """
        # We will do a check for the bios before we do anything else
        self.__check_for_user_supplied_bios__()
        return True if os.path.exists(self.emulator_bios_location())
        # If we get to this point, then the file doesn't exist. We should make
        # a note that this emulator isn't available, and return False
        missing_bios_message = "\
        %s emulator is missing a required BIOS. Please find the bios named \
        '%s' and put it in the %s roms directory under the name %s" % 
        (self._console_name,self._bios_name_,self._console_name_,self.user_supplied_bios_filename)
        log(missing_bios_message,0)
        
    def valid_rom(self,path):
        """
        We ask the user to put the bios in the ROM directory for the console,
        so we need to make sure that Ice doesn't accidently add it as a
        playable game. That would be super awkward.
        """
        romname, romext = os.path.splitext(path)
        if romext == ".bios":
            return False
        return True
        
    def user_supplied_bios_filename(self):
        """
        The user supplied bios should be named "{shortname}.bios"
        
        Example...
        PS1.bios
        PS2.bios
        GBA.bios
        etc...
        """
        return "%s.bios" % self._console_name_

    def user_supplied_bios_location(self):
        """
        The user supplied bios should be in ROMs directory for a given console,
        and should be named what user_supplied_bios_filename describes
        
        Example...
        Windows: C:\Users\Scott\ROMs\PS1\PS1.bios
        Mac OS X: /Users/scottrice/ROMs/PS1/PS1.bios
        """
        return os.path.join(IceFilesystemHelper.roms_directory(),self._console_name_,self.user_supplied_bios_filename())
        
    def emulator_bios_location(self):
        """
        The emulator bios location is the path which the emulator expects the
        bios file to be located
        """
        return os.path.join(self.directory,self._bios_directory_,self._bios_name_)