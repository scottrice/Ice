#!/usr/bin/env python
# encoding: utf-8
"""
platform.py

Created by Scott on 2012-12-24.
Copyright (c) 2012 Scott Rice. All rights reserved.

This file contains functions that help deal with multiple platforms.

Code should be added to this file if it helps support multiple platforms. This
does NOT include code that does platform specific things. A function which gets
a string to represent the platform is a good candidate for this file. A
function that executes some command on windows but some other command on osx
is not a good candidate for this file. In that case, each platform should have
a separate function, and the `platform_specific` function should be used to
select the correct one
"""

import sys


def is_windows():
	return sys.platform.startswith('win')

def is_osx():
	return sys.platform.startswith('darwin')

def is_linux():
    return str(sys.platform).startswith('lin')

def to_string():
    if is_windows():
        return "Windows"
    elif is_osx():
        return "OSX"
    elif is_linux():
        return "Linux"

def _platform_specific_default():
	raise StandardError("The developer didn't test this thoroughly on your platform. Please submit an issue to github.com/scottrice/Ice")

def platform_specific(windows=_platform_specific_default, osx=_platform_specific_default, linux=_platform_specific_default):
	if is_windows():
		return windows
	elif is_osx():
		return osx
	elif is_linux():
		return linux
