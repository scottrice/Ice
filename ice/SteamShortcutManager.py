#!/usr/bin/env python
# encoding: utf-8
"""
SteamShortcutManager.py

Created by Scott on 2012-12-20.
Copyright (c) 2012 Scott Rice. All rights reserved.
"""

import sys
import os

x00 = u'\x00'
x01 = u'\x01'
x08 = u'\x08'
x0a = u'\x0a'

class SteamShortcut:
    def __init__(self,appname,exe,startdir,icon,tag):
        self.appname = appname
        self.exe = exe
        self.startdir = startdir
        self.icon = icon
        self.tag = tag


# This class is in charge of outputting a valid shortcuts.vdf file given an
# array of SteamShortcut objects. This allows normal python code to interact
# with Steam's Non-Steam game list.
class SteamShortcutFileFormatter():
    def generate_string(self,shortcuts):
        string = x00 + 'shortcuts' + x00 + self.generate_array_string(shortcuts) + x08 + x08 + x0a
        # rstrip is to remove the eol character that is automatically added.
        # According to vim the files I got from steam don't have the eol character
        return unicode(string).rstrip()
        
    def generate_array_string(self,shortcuts):
        string = ""
        for i in range(len(shortcuts)):
            shortcut = shortcuts[i]
            string += x00 + str(i) + x00 + self.generate_shortcut_string(shortcut)
        return string
            
    def generate_shortcut_string(self,shortcut):
        string = ""
        string += self.generate_keyvalue_pair("AppName",shortcut.appname)
        string += self.generate_keyvalue_pair("Exe",shortcut.exe)
        string += self.generate_keyvalue_pair("StartDir",shortcut.startdir)
        string += self.generate_icon_string(shortcut.icon)
        # Tags seem to be a special case. It seems to be a key-value pair just
        # like all the others, except it doesnt start with a x01 character. It
        # also seems to be an array, even though Steam wont let more than one
        # be used. I am just going to use a special function to represent this
        # strange case
        string += self.generate_tags_string(shortcut.tag)
        string += x08
        return string
        
    # The 'more' variable was for when I used this function to generate tags
    # I'm not sure if tags are a special case, or if dictionaries keyvalues are
    # supposed to end in x00 when there are more and x08 when there arent. Since
    # I am not sure, I am going to leave the code in for now
    def generate_keyvalue_pair(self,key,value,more=True):
        if value == "":
            value = x00
        return x01 + key + x00 + value + (x00 if more else x08)
    
    def generate_icon_string(self,icon,more=True):
        # if icon == "":
        #     icon = x00
        return x01 + "icon" + x00 + icon + x00 + (x00 if more else x08)
    
    def generate_tags_string(self,tag):
        string = "tags" + x00
        if tag == "":
            string += x08
        else:
            string += self.generate_tag_array_string([tag])
        return string
        
    def generate_tag_array_string(self,tags):
        string = ""
        for i in range(len(tags)):
            tag = tags[i]
            string += x01 + str(i) + x00 + str(tag) + x00 + x08
        return string
        
# This class is in charge of parsing a shortcuts.vdf file into an array which
# can be easily manipulated with python code.
class SteamShortcutFileParser():
    # This is written in the style of a recursive decent parser. There is no
    # real reason why this is the case, other than that is the type of parser I
    # know how to write (thanks compilers class!). I will be basing it on the
    # grammar which I have (hopefully) written above.
    def parse(self,string):
        return []
            

class SteamShortcutManager():
    
    def __init__(self,file=None):
        self.games = []
        if file != None:
            self.__load_shortcuts__(file)
            
    def __load_shortcuts__(self,file):
        self.shortcuts_file = file
        file_contents = open(file,"r").read()
        self.games = SteamShortcutFileParser().parse(file_contents)
        
    def save(self):
        print "Write to file: %s" % self.shortcuts_file
        print self.to_shortcuts_string()
        #open(self.shortcuts_file,"w").write(self.to_shortcuts_string())
            
    def add_game(self,appname,exe,startdir,icon="",tag=""):
        shortcut = SteamShortcut(appname,exe,startdir,icon,tag)
        self.games.append(shortcut)
        
    def to_shortcuts_string(self):
        return SteamShortcutFileFormatter().generate_string(self.games)