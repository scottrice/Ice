"""
backed_object_tests.py

Created by Scott on 2014-08-20.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

import mock
import os
import shutil
import tempfile
import unittest

from ice.persistence.backed_object import BackedObject
from ice.persistence.config_file_backing_store import ConfigFileBackingStore

class BackedObjectTests(unittest.TestCase):
  def setUp(self):
    self.tempdir = tempfile.mkdtemp()
    self.tempfile = os.path.join(self.tempdir, "test.ini")

  def tearDown(self):
    BackedObject.backing_store = None
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

  def test_find_returns_none_with_invalid_identifier(self):
    bs = self.create_backing_store({})
    BackedObject.backing_store = bs
    im = BackedObject.find("Iron Man")
    self.assertIsNone(BackedObject.find("Iron Man"))

  def test_find_returns_non_none_with_valid_identifier(self):
    bs = self.create_backing_store({ "Iron Man": {} })
    BackedObject.backing_store = bs
    self.assertIsNotNone(BackedObject.find("Iron Man"))

  def test_find_returns_same_object_between_calls(self):
    bs = self.create_backing_store({ "Iron Man": {} })
    BackedObject.backing_store = bs
    first_result = BackedObject.find("Iron Man")
    self.assertIsNotNone(first_result)
    second_result = BackedObject.find("Iron Man")
    self.assertIsNotNone(second_result)
    self.assertIs(first_result, second_result)

  def test_find_doesnt_return_new_object_before_save(self):
    bs = self.create_backing_store({})
    BackedObject.backing_store = bs
    war_machine = BackedObject("War Machine")
    war_machine.set_backed_value("identity", "James Rhodes")
    self.assertIsNone(BackedObject.find("War Machine"))

  def test_find_returns_saved_object_after_save(self):
    bs = self.create_backing_store({})
    BackedObject.backing_store = bs
    war_machine = BackedObject("War Machine")
    war_machine.set_backed_value("identity", "James Rhodes")
    war_machine.save()
    self.assertEquals(BackedObject.find("War Machine"), war_machine)

  def test_backed_value(self):
    bs = self.create_backing_store({
      "Iron Man": { "identity": "Tony Stark" }
    })
    BackedObject.backing_store = bs
    iron_man = BackedObject("Iron Man")
    self.assertEquals(iron_man.backed_value("identity"), "Tony Stark")

  def test_set_backed_value(self):
    bs = self.create_backing_store({ "Iron Man": {} })
    BackedObject.backing_store = bs
    iron_man = BackedObject("Iron Man")
    self.assertIsNone(iron_man.backed_value("identity"))
    iron_man.set_backed_value("identity", "Tony Stark")
    self.assertEquals(iron_man.backed_value("identity"), "Tony Stark")

  def test_set_backed_value_doesnt_modify_backing_store(self):
    bs = self.create_backing_store({
      "Iron Man": { "alignment": "good" }
    })
    BackedObject.backing_store = bs
    iron_man = BackedObject("Iron Man")
    self.assertEqual(iron_man.backed_value("alignment"), "good")
    iron_man.set_backed_value("alignment", "questionable")
    self.assertEqual(iron_man.backed_value("alignment"), "questionable")
    self.assertEqual(bs.get("Iron Man", "alignment"), "good")