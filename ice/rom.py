#!/usr/bin/env python
# encoding: utf-8
"""
IceROM.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.

ROM model. Handles the collection of data that makes up a ROM (as of right now,
just the path to the ROM and what console is is from). Also contains some
convenience methods for the filesystem. 

Functionality should be added to this class if it heavily involves the use of
ROMs
"""

import sys
import os
import stat
import unicodedata

import settings
import platform
import filesystem_helper
from steam_shortcut_manager import SteamShortcut

class ROM:
    def __init__(self,path,console):
        self.path = path
        self.console = console

    def __repr__(self):
        return self.name()

    def __eq__(self,other):
        return self.path == other.path and self.console == other.console
        
    def name(self):
        name_with_ext = os.path.basename(self.path)

        # normalize the name to get rid of symbols that break the shortcuts.vdf
        name_with_ext = unicodedata.normalize('NFKD', unicode(name_with_ext.decode('utf-8'))).encode('ascii', 'ignore')

        dot_index = name_with_ext.rfind('.')
        if dot_index == -1:
            # There is no period, so there is no extension. Therefore, the
            # name with extension is the name
            return name_with_ext
        # Return the entire string leading up to (but not including) the period
        return name_with_ext[:dot_index]
        
    def executable_path(self):
        suffix = ".cmd" if sys.platform.startswith('win') else ".sh"
        return os.path.join(self.console.executables_directory(),self.name()+suffix)
        
    def to_shortcut(self):
        command_string = self.console.emulator.command_string(self)
        startdir = self.console.emulator.startdir(self)
        return SteamShortcut(self.name(),command_string,startdir,"",self.console.fullname)
        # Each shortcut should have an icon set based on the console for which
        # it belongs
        # return SteamShortcut(self.name(),command_string,startdir,self.console.icon_path(),self.console.fullname)

    def windows_executable_string(self):
        return "\"%s\" \"%s\"" % (self.console.emulator_path, self.path)

    def osx_executable_string(self):
        # Check if we are running an application or a shell script
        if self.console.emulator.location.endswith(".app"):
            # If we are running an app, we need to do 'open -a {app_path}'
            return "#!/usr/bin/env bash\nopen -a \"%s\" \"%s\"\n" % (self.console.emulator.location, self.path)
        else:
            # If we are running a script, we just execute the script
            return "#!/usr/bin/env bash\n\"%s\" \"%s\"\n" % (self.console.emulator.location,self.path)

    def linux_executable_string(self):
        # If we are running a script, we just execute the script
        return "#!/usr/bin/env bash\n\"%s\" \"%s\"\n" % (self.console.emulator.location,self.path)

    executable_string = platform.platform_specific(windows=windows_executable_string, osx=osx_executable_string, linux=linux_executable_string)
        
    def ensure_exe_file_exists(self):
        """
        Checks to see if a file exists at the executable path, and if it does
        not, then creates the file with the executable_string
        """
        if not os.path.exists(self.executable_path()):
            open(self.executable_path(),"w+").write(self.executable_string())
            # Taken from StackOverflow answer: 
            # http://stackoverflow.com/questions/12791997/how-do-you-do-a-simple-chmod-x-from-within-python
            st = os.stat(self.executable_path())
            os.chmod(self.executable_path(), st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)