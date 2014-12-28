"""
backed_object.py

Created by Scott on 2014-08-14.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

from ice import utils


class BackedObject(object):

  def __init__(self, backing_store, identifier):
    self.backing_store = backing_store
    self.identifier = identifier
    self.dirty_values = {}

  def backed_value(self, key, default=None):
    if key in self.dirty_values:
      return self.dirty_values[key]
    else:
      return self.backing_store.get(self.identifier, key, default)

  def set_backed_value(self, key, value):
    self.dirty_values[key] = value

  def save(self):
    # If this is an entirely new object, add a section for it in the store
    if not self.backing_store.has_identifier(self.identifier):
      self.backing_store.add_identifier(self.identifier)
    # Modify all of the keys/values
    for key in self.dirty_values:
      new_value = self.dirty_values[key]
      self.backing_store.set(self.identifier, key, new_value)
    # Save the store
    self.backing_store.save()
    # After a save no value is dirty
    self.dirty_values = {}
