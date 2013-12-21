#!/usr/bin/env python
# encoding: utf-8
"""
utils.py

Created by Scott on 2013-12-21.
Copyright (c) 2013 Scott Rice. All rights reserved.

Functionality should be added here if it is just general python utility
functions, not related to Ice at all. You should be able to move this file to
another python project and be able to use it out of the box.
"""

def idx(dictionary, index, default=None):
    if index in dictionary:
        return dictionary[index]
    else:
        return default
