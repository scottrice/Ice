"""
backed_object_manager.py

Created by Scott on 2014-08-20.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

from ice.persistence.backed_object import BackedObject


class BackedObjectManager(object):

  def __init__(self, backing_store):
    self.backing_store = backing_store
    self.managed_objects = {}

  def __iter__(self):
    return iter(self.all())

  def all(self):
    return map(self.find, self.backing_store.identifiers());

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

  def new(self, identifier):
    """
    Creates a new instance of an object managed by BackedObjectManager, but
    doesn't save it
    """
    return BackedObject(self.backing_store, identifier)
