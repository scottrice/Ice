# encoding: utf-8
"""
backing_store.py

Created by Scott on 2014-08-12.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

import abc

class BackingStore(object):
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def sections(self):
    """
    Returns a list of section ids that can be used to get key/value information
    from keys/get.
    """
    pass

  @abc.abstractmethod
  def add_section(self, id):
    """
    Adds a section to the BackingStore. Throws an ValueError if a section
    already exists with that id.
    """
    pass

  @abc.abstractmethod
  def remove_section(self, id):
    """
    Removes a section from the BackingStore. Throws a ValueError if no section
    exists with that id
    """
    pass

  @abc.abstractmethod
  def keys(self, section):
    """
    Returns a list of keys inside the section `section`. These keys are such
    that calling `get` with section and any resulting key will give a non-None
    result.
    """
    pass

  @abc.abstractmethod
  def get(self, section, key):
    """
    Returns the value saved for `key` in `section`
    """
    pass

  @abc.abstractmethod
  def set(self, section, key, value):
    """
    Sets the value of `key` in `section` as `value`. This value is guaranteed
    to be the same between
    """
    pass

  @abc.abstractmethod
  def save(self):
    pass
