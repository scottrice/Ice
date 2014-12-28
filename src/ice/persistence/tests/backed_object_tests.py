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

  def test_backed_value(self):
    bs = self.create_backing_store({
        "Iron Man": {"identity": "Tony Stark"}
    })
    iron_man = BackedObject(bs, "Iron Man")
    self.assertEquals(iron_man.backed_value("identity"), "Tony Stark")

  def test_set_backed_value(self):
    bs = self.create_backing_store({"Iron Man": {}})
    iron_man = BackedObject(bs, "Iron Man")
    self.assertIsNone(iron_man.backed_value("identity"))
    iron_man.set_backed_value("identity", "Tony Stark")
    self.assertEquals(iron_man.backed_value("identity"), "Tony Stark")

  def test_set_backed_value_doesnt_modify_backing_store(self):
    bs = self.create_backing_store({
        "Iron Man": {"alignment": "good"}
    })
    iron_man = BackedObject(bs, "Iron Man")
    self.assertEqual(iron_man.backed_value("alignment"), "good")
    iron_man.set_backed_value("alignment", "questionable")
    self.assertEqual(iron_man.backed_value("alignment"), "questionable")
    self.assertEqual(bs.get("Iron Man", "alignment"), "good")
