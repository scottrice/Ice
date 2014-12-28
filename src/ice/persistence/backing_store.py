# encoding: utf-8
"""
backing_store.py

Created by Scott on 2014-08-12.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

import abc


class BackingStore(object):
  __metaclass__ = abc.ABCMeta

  def __init__(self, path):
    self.path = path

  @abc.abstractmethod
  def identifiers(self):
    """
    Returns a list of identifiers that can be used to get key/value information
    from keys/get.
    """
    pass

  def has_identifier(self, ident):
    return ident in self.identifiers()

  @abc.abstractmethod
  def add_identifier(self, ident):
    """
    Adds an identifier to the BackingStore. Throws an ValueError if an
    identifier already exists with that id.
    """
    pass

  @abc.abstractmethod
  def remove_identifier(self, ident):
    """
    Removes an identifier from the BackingStore. Throws a ValueError if no
    section exists with that id
    """
    pass

  @abc.abstractmethod
  def keys(self, ident):
    """
    Returns a list of keys inside the section `section`. These keys are such
    that calling `get` with section and any resulting key will give a non-None
    result.
    """
    pass

  @abc.abstractmethod
  def get(self, ident, key, default=None):
    """
    Returns the value saved for `key` in `section`
    """
    pass

  @abc.abstractmethod
  def set(self, ident, key, value):
    """
    Sets the value of `key` in `section` as `value`. This value is guaranteed
    to be the same between
    """
    pass

  @abc.abstractmethod
  def save(self):
    pass
