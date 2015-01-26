
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

  def test_previous_managed_ids_returns_empty_list_for_missing_file(self):
    missing_path = os.path.join("some", "stupid", "path")
    self.assertFalse(os.path.exists(missing_path))

    archive = ManagedROMArchive(missing_path)
    self.assertEquals(archive.previous_managed_ids(self.mock_user), [])

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
