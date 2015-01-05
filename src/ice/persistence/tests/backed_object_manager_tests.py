"""
backed_object_manager_tests.py

Created by Scott on 2014-08-20.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

import mock
import os
import shutil
import tempfile
import unittest

from ice.persistence.backed_object import BackedObject
from ice.persistence.backed_object_manager import BackedObjectManager
from ice.persistence.config_file_backing_store import ConfigFileBackingStore

# The fact that this class exists should probably signal that my current API
# isn't perfect...
class BackedObjectBackedObjectAdapter(object):
  def new(self, backing_store, identifier):
    return BackedObject(backing_store, identifier)

  def save_in_store(self, backing_store, identifier, obj):
    pass

class BackedObjectManagerTests(unittest.TestCase):

  def setUp(self):
    self.tempdir = tempfile.mkdtemp()
    self.tempfile = os.path.join(self.tempdir, "test.ini")
    self.backing_store = ConfigFileBackingStore(self.tempfile)
    self.manager = BackedObjectManager(self.backing_store, BackedObjectBackedObjectAdapter())

  def tearDown(self):
    shutil.rmtree(self.tempdir)

  def populate_backing_store(self, data):
    for ident in data.keys():
      self.backing_store.add_identifier(ident)
      ident_data = data[ident]
      for key in ident_data.keys():
        value = ident_data[key]
        self.backing_store.set(ident, key, value)
    self.backing_store.save()

  def test_reading_data_from_store(self):
    self.populate_backing_store({
        "Iron Man": {
            "identity": "Tony Stark",
        },
        "War Machine": {
            "identity": "James Rhodes",
            "alias": "Rhodey",
        },
    })
    iron_man = self.manager.find("Iron Man")
    war_machine = self.manager.find("War Machine")

    self.assertIsNotNone(iron_man)
    self.assertEquals(iron_man.identifier, "Iron Man")
    self.assertEquals(iron_man.backed_value("identity"), "Tony Stark")

    self.assertIsNotNone(war_machine)
    self.assertEquals(war_machine.identifier, "War Machine")
    self.assertEquals(war_machine.backed_value("identity"), "James Rhodes")
    self.assertEquals(war_machine.backed_value("alias"), "Rhodey")

  def test_all(self):
    self.populate_backing_store({
        "Iron Man": {},
        "War Machine": {},
    })
    all_objects = self.manager.all()
    self.assertIs(len(all_objects), 2)
    obj1 = all_objects[0]
    obj2 = all_objects[1]
    self.assertFalse(obj1.identifier == obj2.identifier)
    self.assertIn(obj1.identifier, ["Iron Man", "War Machine"])
    self.assertIn(obj2.identifier, ["Iron Man", "War Machine"])

  def test_find_returns_none_with_invalid_identifier(self):
    im = self.manager.find("Iron Man")
    self.assertIsNone(self.manager.find("Iron Man"))

  def test_find_returns_non_none_with_valid_identifier(self):
    self.populate_backing_store({"Iron Man": {}})
    self.assertIsNotNone(self.manager.find("Iron Man"))

  def test_find_returns_same_object_between_calls(self):
    self.populate_backing_store({"Iron Man": {}})
    first_result = self.manager.find("Iron Man")
    self.assertIsNotNone(first_result)
    second_result = self.manager.find("Iron Man")
    self.assertIsNotNone(second_result)
    self.assertIs(first_result, second_result)

  def test_find_after_set_object_for_identifier_returns_same_object_that_was_set(self):
    war_machine = BackedObject(self.backing_store, "War Machine")
    self.manager.set_object_for_identifier(war_machine, "War Machine")
    self.assertEquals(self.manager.find("War Machine"), war_machine)
