"""
backed_object.py

Created by Scott on 2014-08-14.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

from ice import utils

class BackedObject(object):

  backing_store = None
  find_cache = {}

  @classmethod
  def all(cls):
    return [cls.find(ident) for ident in cls.backing_store.identifiers()]

  @classmethod
  def find(cls, ident):
    if cls.backing_store.has_identifier(ident):
      if ident not in cls.find_cache:
        cls.find_cache[ident] = cls(ident)
      return cls.find_cache[ident]
    else:
      return None

  def __init__(self, identifier):
    self.backing_store_identifier = identifier
    self.value_changes = {}

  def backed_value(self, key, default=None):
    if key in self.value_changes:
      return self.value_changes[key]
    else:
      return self.backing_store.get(self.backing_store_identifier, key, default)

  def set_backed_value(self, key, value):
    self.value_changes[key] = value

  def save(self):
    # If this is an entirely new object, add a section for it in the store
    if not self.backing_store.has_identifier(self.backing_store_identifier):
      self.backing_store.add_identifier(self.backing_store_identifier)
    # Modify all of the keys/values
    for key in self.value_changes:
      new_value = self.value_changes[key]
      self.backing_store.set(self.backing_store_identifier, key, new_value)
    # Save the store
    self.backing_store.save()
    # After a save none of the values are `changed`
    self.value_changes = {}
    # We also want to ensure that `find` returns this object now, so put it
    # in the cache
    self.find_cache[self.backing_store_identifier] = self