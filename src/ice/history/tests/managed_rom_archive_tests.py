
import json
import mock
import os
import shutil
import tempfile
import unittest

from ice.history.managed_rom_archive import ManagedROMArchive

class ManagedROMArchiveTests(unittest.TestCase):
  def setUp(self):
    self.tempdir = tempfile.mkdtemp()
    self.temppath = os.path.join(self.tempdir, "tempfile")
    self.mock_user = mock.MagicMock()
    self.mock_user.id32 = 1234

  def tearDown(self):
    shutil.rmtree(self.tempdir)

  def test_previous_managed_ids_returns_none_for_missing_file(self):
    missing_path = os.path.join("some", "stupid", "path")
    self.assertFalse(os.path.exists(missing_path))

    archive = ManagedROMArchive(missing_path)
    self.assertIsNone(archive.previous_managed_ids(self.mock_user))

  def test_previous_managed_ids_raises_exception_for_malformed_json(self):
    with open(self.temppath, "w+") as f:
      f.write("notrealjson")

    with self.assertRaises(ValueError):
      archive = ManagedROMArchive(self.temppath)

  def test_previous_managed_ids_returns_empty_list_for_missing_user(self):
    data = {
      "1337": []
    }
    with open(self.temppath, "w+") as f:
      f.write(json.dumps(data))
    archive = ManagedROMArchive(self.temppath)

    self.assertEquals(archive.previous_managed_ids(self.mock_user), [])

  def test_previous_managed_ids_returns_list_from_json(self):
    data = {
      "1234": [
        "1234567890",
        "0987654321",
      ]
    }
    with open(self.temppath, "w+") as f:
      f.write(json.dumps(data))
    archive = ManagedROMArchive(self.temppath)

    self.assertEquals(archive.previous_managed_ids(self.mock_user), ["1234567890","0987654321"])

  def test_set_managed_ids_creates_new_file_if_needed(self):
    self.assertFalse(os.path.exists(self.temppath))
    archive = ManagedROMArchive(self.temppath)
    archive.set_managed_ids(self.mock_user, ["1234567890"])

    self.assertTrue(os.path.exists(self.temppath))

  def test_previous_managed_ids_returns_new_value_after_set_managed_ids(self):
    archive = ManagedROMArchive(self.temppath)
    new_ids = ["1234567890"]

    self.assertNotEqual(archive.previous_managed_ids(self.mock_user), new_ids)
    archive.set_managed_ids(self.mock_user, ["1234567890"])
    self.assertEqual(archive.previous_managed_ids(self.mock_user), new_ids)

  def test_creating_new_archive_after_set_managed_ids_uses_new_ids(self):
    archive = ManagedROMArchive(self.temppath)
    new_ids = ["1234567890"]

    self.assertNotEqual(archive.previous_managed_ids(self.mock_user), new_ids)
    archive.set_managed_ids(self.mock_user, ["1234567890"])

    new_archive = ManagedROMArchive(self.temppath)
    self.assertEqual(new_archive.previous_managed_ids(self.mock_user), new_ids)
