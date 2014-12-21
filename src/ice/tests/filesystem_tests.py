
import os
import shutil
import tempfile
import unittest

from ice import filesystem

class FilesystemTests(unittest.TestCase):

  def setUp(self):
    self.tempdir = tempfile.mkdtemp()
    self.filesystem = filesystem.Filesystem()

  def tearDown(self):
    shutil.rmtree(self.tempdir)

  def touch_file(self, path, contents="Arbitrary"):
    with open(path, "w") as f:
      f.write(contents)

  def test_is_directory_asserts_when_path_doesnt_exist(self):
    path = os.path.join(self.tempdir, "DNE")
    with self.assertRaises(AssertionError):
      self.filesystem.is_directory(path)

  def test_is_directory_returns_true_for_directories(self):
    path = os.path.join(self.tempdir, "temp_directory")
    os.mkdir(os.path.join(self.tempdir, path))
    self.assertTrue(self.filesystem.is_directory(path))

  def test_is_directory_returns_false_for_files(self):
    path = os.path.join(self.tempdir, "tempfile")
    self.touch_file(path)
    self.assertFalse(self.filesystem.is_directory(path))

  def test_files_in_directory_asserts_when_directory_doesnt_exist(self):
    path = os.path.join(self.tempdir, "DNE")
    with self.assertRaises(AssertionError):
      self.filesystem.files_in_directory(path)

  def test_files_in_directory_asserts_when_given_path_is_a_file(self):
    path = os.path.join(self.tempdir, "tempfile")
    self.touch_file(path)
    with self.assertRaises(AssertionError):
      self.filesystem.files_in_directory(path)

  def test_files_in_directory_only_returns_files(self):
    file1 = os.path.join(self.tempdir, "file1")
    self.touch_file(file1)
    file2 = os.path.join(self.tempdir, "file2")
    self.touch_file(file2)
    dir1 = os.path.join(self.tempdir, "dir1")
    os.mkdir(dir1)
    dir2 = os.path.join(self.tempdir, "dir2")
    os.mkdir(dir2)
    self.assertEquals(self.filesystem.files_in_directory(self.tempdir), [file1, file2])

  def test_files_in_directory_doesnt_return_hidden_files(self):
    file1 = os.path.join(self.tempdir, "bluefile")
    self.touch_file(file1)
    file2 = os.path.join(self.tempdir, "redfile")
    self.touch_file(file2)
    hidden_file = os.path.join(self.tempdir, ".hidden_file")
    self.touch_file(hidden_file)
    dir1 = os.path.join(self.tempdir, "dir1")
    os.mkdir(dir1)
    dir2 = os.path.join(self.tempdir, "dir2")
    os.mkdir(dir2)
    self.assertEquals(self.filesystem.files_in_directory(self.tempdir), [file1, file2])

  def test_subdirectories_of_directory_asserts_when_directory_doesnt_exist(self):
    path = os.path.join(self.tempdir, "DNE")
    with self.assertRaises(AssertionError):
      self.filesystem.subdirectories_of_directory(path)

  def test_subdirectories_of_directory_asserts_when_given_path_is_a_file(self):
    path = os.path.join(self.tempdir, "tempfile")
    self.touch_file(path)
    with self.assertRaises(AssertionError):
      self.filesystem.subdirectories_of_directory(path)

  def test_subdirectories_of_directory_only_returns_directories(self):
    file1 = os.path.join(self.tempdir, "file1")
    self.touch_file(file1)
    file2 = os.path.join(self.tempdir, "file2")
    self.touch_file(file2)
    dir1 = os.path.join(self.tempdir, "dir1")
    os.mkdir(dir1)
    dir2 = os.path.join(self.tempdir, "dir2")
    os.mkdir(dir2)
    self.assertEquals(self.filesystem.subdirectories_of_directory(self.tempdir), [dir1, dir2])
