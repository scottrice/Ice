#!/usr/bin/env python
# encoding: utf-8
"""
steam_shortcut_manager.py

Created by Scott on 2012-12-20.
Copyright (c) 2012 Scott Rice. All rights reserved.
"""

import sys
import os

import re

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
        
    def __eq__(self,other):
        return (
            isinstance(other,self.__class__) and
            self.appname == other.appname and
            self.exe == other.exe and
            self.startdir == other.startdir and
            self.icon == other.icon and
            self.tag == other.tag
        )
    
    def __ne__(self,other):
        return not self.__eq__(other)
        
    def __hash__(self):
        return "__STEAMSHORTCUT{0}{1}{2}{3}{4}__".format(self.appname,self.exe,self.startdir,self.icon,self.tag).__hash__()
        
    def __repr__(self):
        return "Steam Shortcut: %s" % self.appname


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
        string += self.generate_keyvalue_pair("icon",shortcut.icon)
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
        return x01 + key + x00 + value + (x00 if more else x08)
    
    def generate_tags_string(self,tag):
        string = x00 + "tags" + x00
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
    # I am going to use regular expressions to parse this file. I haven't used
    # regular expressions in Python before, so I apologize for any terrible
    # code that I write...
    def parse(self,string):
        return self.match_base(string)
        
    def match_base(self,string):
        match = re.match(ur"\u0000shortcuts\u0000(.*)\u0008\u0008$",string, re.IGNORECASE)
        if match:
            return self.match_array_string(match.groups()[0])
        else:
            return None
    
    def match_array_string(self,string):
        # Match backwards (aka match last item first)
        if string == "":
            return []
        # One side effect of matching this way is we are throwing away the
        # array index. I dont think that it is that important though, so I am
        # ignoring it for now
        shortcuts = []
        while True:
            match = re.match(ur"(.*)\u0000[0-9]+\u0000(\u0001AppName.*)\u0008",string, re.IGNORECASE)
            if match:
                groups = match.groups()
                string = groups[0]
                shortcuts.append(self.match_shortcut_string(groups[1]))
            else:
                shortcuts.reverse()
                return shortcuts
            
    def match_shortcut_string(self,string):
        # I am going to cheat a little here. I am going to match specifically
        # for the shortcut string (Appname, Exe, StartDir, etc), as oppposed
        # to matching for general Key-Value pairs. This could possibly create a
        # lot of work for me later, but for now it will get the job done
        match = re.match(ur"\u0001AppName\u0000(.*)\u0000\u0001Exe\u0000(.*)\u0000\u0001StartDir\u0000(.*)\u0000\u0001icon\u0000(.*)\u0000\u0000tags\u0000(.*)\u0008",string, re.IGNORECASE)
        if match:
            # The 'groups' that are returned by the match should be the data
            # contained in the file. Now just make a SteamShortcut out of that
            # data
            groups = match.groups()
            appname = groups[0]
            exe = groups[1]
            startdir = groups[2]
            icon = groups[3]
            tags = self.match_tags_string(groups[4])
            return SteamShortcut(appname,exe,startdir,icon,tags)
        else:
            return None
            
    def match_tags_string(self,string):
        match = re.match(ur"\u00010\u0000(.*)\u0000",string)
        if match:
            groups = match.groups()
            return groups[0]
        else:
            return ""

class SteamShortcutManager():
    
    def __init__(self,file=None):
        self.shortcuts = []
        if file != None:
            self.__load_shortcuts__(file)
            
    def __eq__(self,other):
        return (isinstance(other,self.__class__) and self.shortcuts == other.shortcuts)
        
    def __ne__(self,other):
        return not self.__eq__(other)
            
    def __load_shortcuts__(self,file):
        self.shortcuts_file = file
        try:
            file_contents = open(file,"r").read()
            parsed_shortcuts = SteamShortcutFileParser().parse(file_contents)
            if parsed_shortcuts == None:
                print "Parsing error on file: %s" % file
        except IOError:
            file_contents = ""
            parsed_shortcuts = []
        self.shortcuts = parsed_shortcuts
        # self.games = SteamShortcutFileParser().parse(file_contents)
        
    def save(self,file=None):
        # print "Write to file: %s" % self.shortcuts_file
        # print self.to_shortcuts_string()
        # If they just called save(), then overwrite the file that was used to
        # generate the manager.
        if not file:
            file = self.shortcuts_file
        # If file is still undefined, then we have no idea where to save it, so
        # we just return after printing an error
        if not file:
            print "SteamShortcutManager Save Error: No file specified"
            return None
        open(file,"w").write(self.to_shortcuts_string())
    
    def add(self,shortcut):
        self.shortcuts.append(shortcut) 
            
    def add_shortcut(self,appname,exe,startdir,icon="",tag=""):
        shortcut = SteamShortcut(appname,exe,startdir,icon,tag)
        self.add(shortcut)
        
    def to_shortcuts_string(self):
        return SteamShortcutFileFormatter().generate_string(self.shortcuts)