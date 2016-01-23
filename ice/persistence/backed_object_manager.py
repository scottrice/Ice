"""
backed_object_manager.py

Created by Scott on 2014-08-20.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

from ice.persistence.backed_object import BackedObject


class BackedObjectManager(object):

  def __init__(self, backing_store, model_adapter):
    self.backing_store = backing_store
    self.adapter = model_adapter
    self.managed_objects = {}

  def __iter__(self):
    return iter(self.all())

  def all(self):
    # Since not all identifiers are guaranteed to return full objects, we
    # filter out any `None` elements before returning
    return filter(None, map(self.find, self.backing_store.identifiers()));

  def new(self, identifier):
    obj = self.adapter.new(self.backing_store, identifier)
    if self.adapter.verify(obj):
      return obj

  def find(self, identifier):
    if identifier not in self.backing_store.identifiers():
      return None

    # See if we have a cached version from before
    if identifier in self.managed_objects:
      return self.managed_objects[identifier]

    # If not, create it lazily
    obj = self.new(identifier)
    self.managed_objects[identifier] = obj
    return obj

  def set_object_for_identifier(self, obj, identifier):
    self.managed_objects[identifier] = obj
    # Ensure that the identifier exists in the backing store before we ask
    # the adapter to save it
    if not self.backing_store.has_identifier(identifier):
      self.backing_store.add_identifier(identifier)
    # Make the adapter do the actual saving
    self.adapter.save_in_store(self.backing_store, identifier, obj)
