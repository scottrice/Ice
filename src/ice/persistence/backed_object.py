"""
backed_object.py

Created by Scott on 2014-08-14.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

import abc
from ice import utils

class BackedObject(object):
  __metaclass__ = abc.ABCMeta

  backing_store = None

  @classmethod
  def all(cls):
    return [cls.find(ident) for ident in cls.backing_store.identifiers()]

  @classmethod
  @utils.memoize
  def find(cls, ident):
    return cls(ident) if cls.backing_store.has_identifier(ident) else None

  def __init__(self, identifier):
    self.backing_store_identifier = identifier

  def backed_value(self, key, default=None):
    return self.backing_store.get(self.backing_store_identifier, key, default)
