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

import os
import tempfile
import shutil

import abc

class Emulator(object):
    __metaclass__ = abc.ABCMeta
    
    # directory should be set by any subclasses which manage where emulators
    # are stored (such as the Downloaded Emulator class)
    directory = ""
    
    # Location should be set by any subclasses which manage where emulators
    # are stored (such as the Downloaded Emulator class)
    location = ""
        
    def __init__(self, name, location, format):
        self.name = name
        self.location = location
        self.format = format

    def __add_quotes_if_needed__(self, string):
        if string.startswith("\"") and string.endswith("\""):
            return string
        else:
            return "\"%s\"" % string

    def is_functional(self):
        """
        A basic emulator is always functional.
        """
        return True
    
    def command_string(self, rom):
        """Generates a command string using the format specified by the user"""
        # We don't know if the user put quotes around the emulator location. If
        # so, we dont want to add another pair and screw things up.
        quoted_location = self.__add_quotes_if_needed__(os.path.expanduser(self.location))
        # The user didnt give us the ROM information, but screw it, I already
        # have some code to add quotes to a string, might as well use it.
        quoted_rom = self.__add_quotes_if_needed__(rom.path)
        return self.format.replace("%l", quoted_location).replace("%r", quoted_rom)
        
    def startdir(self,rom):
        """
        Returns the directory which stores the emulator. This value is useful
        as the 'StartDir' option of a Steam Shortcut
        """
        return os.path.dirname(self.location)
        
    def replace_contents_of_file(self,file_path,replacement_function):
        """
        Replaces the contents of a file with the results of replacement_function
        
        'replacement_function' is a function which takes a line of input and
        returns another line, which gets put in the new file.
        """
        # Code mainly taken from:
        # http://stackoverflow.com/questions/39086/search-and-replace-a-line-in-a-file-in-python
        fh, abs_path = tempfile.mkstemp()
        new_file = open(abs_path,'w')
        old_file = open(file_path)
        for line in old_file:
            new_file.write(replacement_function(line))
        # Close handles
        new_file.close()
        os.close(fh)
        old_file.close()
        # Replace file_path with new file
        os.remove(file_path)
        shutil.move(abs_path, file_path)
