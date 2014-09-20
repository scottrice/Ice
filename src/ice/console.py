#!/usr/bin/env python
# encoding: utf-8
"""
console.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.

This class represents the Console datatype. Each ROM is associated with a
Console, and each Console has many ROMs. A Console also is associated with an
emulator, which can be used to play a ROM.

Functionality should be added to this class/module if it deals with Consoles or
their emulators. This includes finding a list of ROMs in this console's folder.
"""

import os

import filesystem_helper
import utils
from persistence.backed_object import BackedObject
from persistence.config_file_backing_store import ConfigFileBackingStore
from emulator import Emulator
from rom import ROM

class Console(BackedObject):
    def __init__(self, backing_store, identifier, config):
        super(Console, self).__init__(backing_store, identifier)
        self.config                 = config

        self.fullname               = identifier
        self.shortname              = self.backed_value('nickname', self.fullname)
        self.extensions             = self.backed_value('extensions', "")
        self.custom_roms_directory  = self.backed_value('roms directory', "")
        self.prefix                 = self.backed_value('prefix', "")
        self.icon                   = self.backed_value('icon', "")
        self.images_directory       = self.backed_value('images directory', "")
        self.emulator_identifier    = self.backed_value('emulator', "")
        
        self.icon = os.path.expanduser(self.icon)
        self.custom_roms_directory = os.path.expanduser(self.custom_roms_directory)
        self.images_directory = os.path.expanduser(self.images_directory)

        self.emulator = config.emulator_manager.find(self.emulator_identifier)

    def __repr__(self):
        return self.fullname

    def is_enabled(self):
        if self.emulator is None:
            return False
        if self.custom_roms_directory and not filesystem_helper.available_to_use(self.custom_roms_directory, create_if_needed=True):
            return False
        return True

    def roms_directory(self):
        """
        If the user has specified a ROMs directory in consoles.txt and it is
        accessible to Ice, returns that.

        Otherwise, appends the shortname of the console to the default ROMs
        directory given by config.txt.
        """
        if self.custom_roms_directory:
            return self.custom_roms_directory
        return os.path.join(self.config.roms_directory(),self.shortname)
      
    def is_valid_rom(self,path):
        """
        This function determines if a given path is actually a valid ROM file.
        If a list of extensions is supplied for this console, we check if the path has a valid extension
        If no extensions are defined for this console, we just accept any file
        """

        if self.extensions == "":
            return True
        extension = os.path.splitext(path)[1].lower()
        return any(extension == ('.'+x.strip().lower()) for x in self.extensions.split(','))
  
    def find_roms(self):
        """
        Reads a list of all the ROMs from the appropriate directory for the
        console
        """
        roms = []
        if not os.path.exists(self.roms_directory()):
            # TODO: Tell the user when we are about to create a directory for them
            # TODO: Why the hell are we checking for and creating directories inside of `find_roms`?
            os.makedirs(self.roms_directory())
        for filename in os.listdir(self.roms_directory()):
            file_path = os.path.join(self.roms_directory(),filename)
            if not os.path.isdir(file_path):
                # On Linux/OSX, we want to make sure hidden files don't get
                # accidently added as well
                if not utils.is_windows() and filename.startswith('.'):
                    continue
                if self.emulator is not None and not self.is_valid_rom(file_path):
                    # TODO: Tell the user that we are ignoring this file
                    # TODO: Again, why the hell are we logging that here?????
                    continue
                roms.append(ROM(file_path,self))
        return roms
