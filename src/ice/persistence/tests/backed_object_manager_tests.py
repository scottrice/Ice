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

# from ice.persistence.backed_object import BackedObject
from ice.persistence.backed_object_manager import BackedObjectManager
from ice.persistence.config_file_backing_store import ConfigFileBackingStore

class BackedObjectManagerTests(unittest.TestCase):
  def setUp(self):
    self.tempdir = tempfile.mkdtemp()
    self.tempfile = os.path.join(self.tempdir, "test.ini")

  def tearDown(self):
    shutil.rmtree(self.tempdir)

  def create_backing_store(self, data):
    bs = ConfigFileBackingStore(self.tempfile)
    for ident in data.keys():
      bs.add_identifier(ident)
      ident_data = data[ident]
      for key in ident_data.keys():
        value = ident_data[key]
        bs.set(ident, key, value)
    bs.save()
    return bs

  def test_initialize_loads_from_store(self):
    bs = self.create_backing_store({
      "Iron Man": {
        "identity": "Tony Stark",
      },
      "War Machine": {
        "identity": "James Rhodes",
        "alias": "Rhodey",
      },
    })
    manager = BackedObjectManager(bs)
    manager.initialize()
    iron_man = manager.find("Iron Man")
    war_machine = manager.find("War Machine")

    self.assertIsNotNone(iron_man)
    self.assertEquals(iron_man.identifier, "Iron Man")
    self.assertEquals(iron_man.backed_value("identity"), "Tony Stark")

    self.assertIsNotNone(war_machine)
    self.assertEquals(war_machine.identifier, "War Machine")
    self.assertEquals(war_machine.backed_value("identity"), "James Rhodes")
    self.assertEquals(war_machine.backed_value("alias"), "Rhodey")
  
  def test_no_objects_from_store_before_initialize(self):
    bs = self.create_backing_store({
      "Iron Man": {
        "identity": "Tony Stark",
      },
      "War Machine": {
        "identity": "James Rhodes",
        "alias": "Rhodey",
      },
    })
    manager = BackedObjectManager(bs)
    iron_man = manager.find("Iron Man")
    war_machine = manager.find("War Machine")

    self.assertIsNone(iron_man)
    self.assertIsNone(war_machine)

  def test_all(self):
    bs = self.create_backing_store({
      "Iron Man": {},
      "War Machine": {},
    })
    manager = BackedObjectManager(bs)
    manager.initialize()
    all_objects = manager.all()
    self.assertIs(len(all_objects), 2)
    obj1 = all_objects[0]
    obj2 = all_objects[1]
    self.assertFalse(obj1.identifier == obj2.identifier)
    self.assertIn(obj1.identifier, ["Iron Man", "War Machine"])
    self.assertIn(obj2.identifier, ["Iron Man", "War Machine"])

  def test_find_returns_none_with_invalid_identifier(self):
    bs = self.create_backing_store({})
    manager = BackedObjectManager(bs)
    manager.initialize()
    im = manager.find("Iron Man")
    self.assertIsNone(manager.find("Iron Man"))

  def test_find_returns_non_none_with_valid_identifier(self):
    bs = self.create_backing_store({ "Iron Man": {} })
    manager = BackedObjectManager(bs)
    manager.initialize()
    self.assertIsNotNone(manager.find("Iron Man"))

  def test_find_returns_same_object_between_calls(self):
    bs = self.create_backing_store({ "Iron Man": {} })
    manager = BackedObjectManager(bs)
    manager.initialize()
    first_result = manager.find("Iron Man")
    self.assertIsNotNone(first_result)
    second_result = manager.find("Iron Man")
    self.assertIsNotNone(second_result)
    self.assertIs(first_result, second_result)

  def test_find_doesnt_return_object_made_with_new(self):
    bs = self.create_backing_store({})
    manager = BackedObjectManager(bs)
    manager.initialize()
    war_machine = manager.new("War Machine")
    war_machine.set_backed_value("identity", "James Rhodes")
    self.assertIsNone(manager.find("War Machine"))

  def test_find_returns_object_made_with_create(self):
    bs = self.create_backing_store({})
    manager = BackedObjectManager(bs)
    manager.initialize()
    war_machine = manager.create("War Machine")
    self.assertEquals(manager.find("War Machine"), war_machine)