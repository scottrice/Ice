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

import appdirs
import collections
import functools
import psutil
import sys

# Convenient function to check if a key is in a dictionary. If so, uses that,
# otherwise, uses the default.
# Also, 'idx' stands for 'index'.
def idx(dictionary, index, default=None):
    if index in dictionary:
        return dictionary[index]
    else:
        return default

def app_data_directory():
    # Parameters are 'App Name' and 'App Author'
    # TODO: Get these values from the same place as setup.py
    return appdirs.user_data_dir("Ice","Scott Rice")

def steam_is_running():
    for pid in psutil.pids():
      try:
        p = psutil.Process(pid)
        if p.name().lower().startswith('steam'):
          return True
      except Exception:
        continue
    return False

def is_windows():
	  return sys.platform.startswith('win')

def is_osx():
	  return sys.platform.startswith('darwin')

def is_linux():
    return str(sys.platform).startswith('lin')

# Decorator for memoization
# Copied from https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
class memoize(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__

    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)
