# encoding: utf-8
"""
_shortcut_generator.py

Created by Scott on 2013-12-29.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os

x00 = b'\x00'
x01 = b'\x01'
x08 = b'\x08'
x0a = b'\x0a'


class ShortcutGenerator(object):

    def to_string(self, shortcuts):
        string = x00 + b'shortcuts' + x00 + self.generate_array_string(shortcuts) + x08 + x08 + x0a
        # rstrip is to remove the eol character that is automatically added.
        # According to vim the files I got from steam don't have the eol character
        return str(string).rstrip()

    def generate_array_string(self, shortcuts):
        string = b""
        for i, shortcut in enumerate(shortcuts):
            string += x00 + str(i).encode() + x00 + self.generate_shortcut_string(shortcut)
        return string

    def generate_shortcut_string(self, shortcut):
        string = b""
        string += self.generate_keyvalue_pair(b"AppName", shortcut.name)
        string += self.generate_keyvalue_pair(b"Exe", shortcut.exe)
        string += self.generate_keyvalue_pair(b"StartDir", shortcut.startdir)
        string += self.generate_keyvalue_pair(b"icon", shortcut.icon)
        # Tags seem to be a special case. It seems to be a key-value pair just
        # like all the others, except it doesnt start with a x01 character. It
        # also seems to be an array, even though Steam wont let more than one
        # be used. I am just going to use a special function to represent this
        # strange case
        string += self.generate_tags_string(shortcut.tags)
        string += x08
        return string

    # The 'more' variable was for when I used this function to generate tags
    # I'm not sure if tags are a special case, or if dictionaries keyvalues are
    # supposed to end in x00 when there are more and x08 when there arent. Since
    # I am not sure, I am going to leave the code in for now
    def generate_keyvalue_pair(self, key: bytes, value: str, more=True):
        return x01 + key + x00 + value.encode() + (x00 if more else x08)

    def generate_tags_string(self, tags):
        string = x00 + b"tags" + x00
        string += self.generate_tag_array_string(tags)
        return string

    def generate_tag_array_string(self, tags):
        string = b""
        for i in range(len(tags)):
            tag = tags[i]
            string += x01 + str(i).encode() + x00 + str(tag).encode() + x00
        return string + x08