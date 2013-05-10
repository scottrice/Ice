#!/usr/bin/env python
# encoding: utf-8
"""
winproject64.py

Created by Scott on 2013-01-07.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os

if sys.platform.startswith('win'):
    import _winreg as registry

import downloaded_emulator

class WinProject64(downloaded_emulator.DownloadedEmulator):
    
    def __init__(self,console_name):
        super(WinProject64,self).__init__(console_name)
    
    def command_string(self,rom):
        """
        The command string format for Project 64 is just...
        \"C:\Path\To\Project64\" C:\Path\To\ROM
        
        Notice the quotes around the path to Project 64, but the lack of quotes
        around the path to the ROM. This is intended in PJ64 1.6.
        
        Since we need to get the keybindings correct, Project64 needs a 
        launcher. The launcher has no such qualms about quotes, and so the
        standard
        \"C:\Path\To\Project64\" \"C:\Path\To\ROM\"
        
        works fine
        """
        return "\"%s\" \"%s\"" % (self.location,rom.path)

    def set_control_scheme(self,controls):
        # Open the keys in a way to set them
        self.set_device(controls["device"])
        controls.pop("device",None)
        regkey = registry.CreateKeyEx(registry.HKEY_CURRENT_USER,"Software\JaboSoft\Project64 DLL\DirectInput7 1.6\Keys 0",0,registry.KEY_SET_VALUE)
        for control,value in controls.iteritems():
            key_name = self.reg_key_for_control(control)
            if value != "":
                registry.SetValueEx(regkey,key_name,0,registry.REG_DWORD,int(value))

    def set_device(self,device):
        regkey = registry.CreateKeyEx(registry.HKEY_CURRENT_USER,"Software\JaboSoft\Project64 DLL\DirectInput7 1.6",0,registry.KEY_SET_VALUE)
        # I decode the string here so that the user can enter in things like
        # \xDE to insert the binary 11011110. This is about the best I can do in
        # terms of letting a user input freeform binary...
        decoded = device.decode("string-escape")
        if decoded != "":
            registry.SetValueEx(regkey,"di.DeviceGUID(0)",0,registry.REG_BINARY,decoded)

    def reg_key_for_control(self,control):
        return {
            "up":"AnalogUp",
            "down":"AnalogDown",
            "left":"AnalogLeft",
            "right":"AnalogRight",
            "start":"Start",
            "a":"A",
            "b":"B",
            "l":"L",
            "r":"R",
            "z":"Z",
            "c-up":"C_Up",
            "c-down":"C_Down",
            "c-left":"C_Left",
            "c-right":"C_Right",
            "d-up":"DigitalUp",
            "d-down":"DigitalDown",
            "d-left":"DigitalLeft",
            "d-right":"DigitalRight",

        }[control]