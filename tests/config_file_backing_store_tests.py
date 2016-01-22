"""
config_file_backing_store_tests.py

Created by Scott on 2014-08-19.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

import os
import shutil
import stat
import tempfile
import unittest

from ice.persistence.config_file_backing_store import ConfigFileBackingStore


class ConfigFileBackingStoreTests(unittest.TestCase):

  def setUp(self):
    self.tempdir = tempfile.mkdtemp()
    self.tempfile = os.path.join(self.tempdir, "test.ini")

  def tearDown(self):
    shutil.rmtree(self.tempdir)

  def create_config_file(self, path, sections_dict):
    # This will write a ConfigFile at `path` with the sections/keys/values
    # pulled from keys/values of the nested section dicitionary
    #
    # A dictionary like this:
    # {
    #   "Section Name": {
    #     "key":value,
    #     "key":value,
    #     ...
    #   },
    #   "Section Name 2": {
    #     "key2":value,
    #     "key2":value,
    #     ...
    #   },
    #   ...
    # }
    #
    # Will produce an output like this
    # [Section Name]
    # key=value
    # key=value
    #
    # [Section Name 2]
    # key2=value
    # key2=value
    f = open(path, "w")
    for section_name in sections_dict.keys():
      f.write("[%s]\n" % section_name)
      keyvalues = sections_dict[section_name]
      for key in keyvalues.keys():
        value = keyvalues[key]
        f.write("%s=%s\n" % (key, value))
      f.write("\n")
    f.close()

  def file_contents(self, path):
    f = open(path, "r")
    contents = f.read()
    f.close()
    return contents

  def test_empty_file(self):
    self.create_config_file(self.tempfile, {})
    cfbs = ConfigFileBackingStore(self.tempfile)
    self.assertEquals(cfbs.identifiers(), [])

  def test_identifiers(self):
    self.create_config_file(self.tempfile, {
        "Iron Man": {},
        "Whiplash": {},
    })
    cfbs = ConfigFileBackingStore(self.tempfile)
    self.assertEquals(cfbs.identifiers(), ["Iron Man", "Whiplash"])

  def test_added_identifiers_show_up_in_subsequent_calls(self):
    self.create_config_file(self.tempfile, {})
    cfbs = ConfigFileBackingStore(self.tempfile)
    cfbs.add_identifier("Iron Man")
    self.assertIn("Iron Man", cfbs.identifiers())

  def test_removed_identifiers_dont_show_up_in_subsequent_calls(self):
    self.create_config_file(self.tempfile, {"Iron Man": {}})
    cfbs = ConfigFileBackingStore(self.tempfile)
    cfbs.remove_identifier("Iron Man")
    self.assertNotIn("Iron Man", cfbs.identifiers())

  def test_add_identifier_raises_valueerror_when_identifier_exists(self):
    self.create_config_file(self.tempfile, {"Iron Man": {}})
    cfbs = ConfigFileBackingStore(self.tempfile)
    with self.assertRaises(ValueError):
      cfbs.add_identifier("Iron Man")

  def test_remove_identifier_does_nothing_when_identifer_dne(self):
    self.create_config_file(self.tempfile, {})
    cfbs = ConfigFileBackingStore(self.tempfile)
    self.assertNotIn("Iron Man", cfbs.identifiers())
    cfbs.remove_identifier("Iron Man")
    self.assertNotIn("Iron Man", cfbs.identifiers())

  def test_keys_raises_valueerror_when_section_dne(self):
    self.create_config_file(self.tempfile, {})
    cfbs = ConfigFileBackingStore(self.tempfile)
    with self.assertRaises(ValueError):
      cfbs.keys("Iron Man")

  def test_get(self):
    self.create_config_file(self.tempfile, {"Iron Man": {
        "identity": "Tony Stark",
        "alignment": "good",
    }})
    cfbs = ConfigFileBackingStore(self.tempfile)
    self.assertEqual(cfbs.get("Iron Man", "identity", ""), "Tony Stark")

  def test_get_returns_default_when_key_dne(self):
    self.create_config_file(self.tempfile, {"Iron Man": {}})
    cfbs = ConfigFileBackingStore(self.tempfile)
    self.assertEqual(cfbs.get("Iron Man", "identity", ""), "")

  def test_get_returns_default_when_section_dne(self):
    self.create_config_file(self.tempfile, {"Iron Man": {}})
    cfbs = ConfigFileBackingStore(self.tempfile)
    self.assertEqual(cfbs.get("Superman", "identity", "Unknown"), "Unknown")

  def test_get_returns_empty_string_when_value_is_emptry_string(self):
    self.create_config_file(self.tempfile, {"Iron Man": {
        "identity": ""
    }})
    cfbs = ConfigFileBackingStore(self.tempfile)
    self.assertEqual(cfbs.get("Iron Man", "identity", "Unknown"), "")

  def test_get_keys_are_case_insensitive(self):
    self.create_config_file(self.tempfile, {"Iron Man": {
        "identity": "Tony Stark",
        "alignment": "good",
    }})
    cfbs = ConfigFileBackingStore(self.tempfile)
    self.assertEqual(cfbs.get("Iron Man", "IDENTITY", ""), "Tony Stark")

  def test_set_keys_are_case_insensitive(self):
    self.create_config_file(self.tempfile, {"Iron Man": {}})
    cfbs = ConfigFileBackingStore(self.tempfile)
    cfbs.set("Iron Man", "identity", "Tony Stark")
    self.assertEqual(cfbs.get("Iron Man", "IDENTITY", ""), "Tony Stark")

  def test_save_creates_new_file_when_path_originally_dne(self):
    self.assertFalse(os.path.isfile(self.tempfile))
    cfbs = ConfigFileBackingStore(self.tempfile)
    cfbs.add_identifier("Iron Man")
    cfbs.set("Iron Man", "identity", "Tony Stark")
    cfbs.save()
    self.assertTrue(os.path.isfile(self.tempfile))

  def test_save_modifies_contents_of_file(self):
    self.create_config_file(self.tempfile, {
        "Iron Man": {"identity": "Tony Stark"}
    })
    old_contents = self.file_contents(self.tempfile)
    cfbs = ConfigFileBackingStore(self.tempfile)
    cfbs.set("Iron Man", "alignment", "good")
    cfbs.add_identifier("Whiplash")
    cfbs.set("Whiplash", "alignment", "evil")
    cfbs.save()
    new_contents = self.file_contents(self.tempfile)
    self.assertNotIn("Whiplash", old_contents)
    self.assertIn("Whiplash", new_contents)
    self.assertNotIn("alignment", old_contents)
    self.assertIn("alignment", new_contents)
    self.assertIn("good", new_contents)
    self.assertIn("evil", new_contents)

  def test_save_raises_ioerror_when_cant_make_new_file(self):
    temppath = os.path.join(self.tempdir, "extra", "directories", "test.ini")
    cfbs = ConfigFileBackingStore(temppath)
    cfbs.add_identifier("Iron Man")
    cfbs.set("Iron Man", "identity", "Tony Stark")
    with self.assertRaises(IOError):
      cfbs.save()

  def test_config_file_backing_store_can_read_saved_file(self):
    cfbs = ConfigFileBackingStore(self.tempfile)
    cfbs.add_identifier("Iron Man")
    cfbs.set("Iron Man", "alignment", "good")
    cfbs.add_identifier("Whiplash")
    cfbs.set("Whiplash", "alignment", "evil")
    cfbs.save()
    new_cfbs = ConfigFileBackingStore(self.tempfile)
    self.assertIn("Iron Man", new_cfbs.identifiers())
    self.assertIn("Whiplash", new_cfbs.identifiers())
    self.assertEquals("good", new_cfbs.get("Iron Man", "alignment"))
    self.assertEquals("evil", new_cfbs.get("Whiplash", "alignment"))

  def test_raises_ioerror_when_permission_denied(self):
    self.create_config_file(self.tempfile, {})
    mode = os.stat(self.tempfile)[stat.ST_MODE]
    new_mode = mode & ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH
    os.chmod(self.tempfile, new_mode)
    cfbs = ConfigFileBackingStore(self.tempfile)
    cfbs.add_identifier("Iron Man")
    cfbs.set("Iron Man", "identity", "Tony Stark")
    with self.assertRaises(IOError):
      cfbs.save()
