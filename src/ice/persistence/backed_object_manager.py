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
    self.initialized = False

  def __iter__(self):
    return iter(self.all())

  def all(self):
    return self.managed_objects.values()

  def find(self, identifier):
    if identifier in self.managed_objects:
      return self.managed_objects[identifier]
    else:
      return None

  def initialize(self):
    """
    Initializes the object manager with all of data that exists in the
    backing store
    """
    if self.initialized:
      return
    for identifier in self.backing_store.identifiers():
      self.create(identifier)
    self.initialized = True

  def new(self, identifier):
    """
    Creates a new instance of an object managed by BackedObjectManager, but
    doesn't save it
    """
    return BackedObject(self.backing_store, identifier)

  def create(self, identifier):
    """
    Creates a new instance of an object managed by BackedObjectManager, saves
    it, and adds it to the BackedObjectManager, ensuring that it will be
    returned again by find
    """
    obj = self.new(identifier)
    obj.save()
    self.add(obj)
    return obj

  def add(self, backed_object):
    """
    Add a `backed_object` to the list of objects this manages.
    """
    self.managed_objects[backed_object.identifier] = backed_object
