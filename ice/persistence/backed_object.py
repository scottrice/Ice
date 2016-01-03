"""
backed_object.py

Created by Scott on 2014-08-14.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

class BackedObject(object):

  def __init__(self, backing_store, identifier):
    self.backing_store = backing_store
    self.identifier = identifier

  def backed_value(self, key, default=None):
    return self.backing_store.get(self.identifier, key, default)
