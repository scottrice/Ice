
import os
import shutil
import sys
import tempfile
import unittest

from nose_parameterized import parameterized

from ice import filesystem


class FilesystemTests(unittest.TestCase):

  def setUp(self):
    self.tempdir = tempfile.mkdtemp()
    self.filesystem = filesystem.RealFilesystem()

  def tearDown(self):
    shutil.rmtree(self.tempdir)

  def touch_file(self, path, contents="Arbitrary"):
    with open(path, "w") as f:
      f.write(contents)

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
    self.assertEquals(
        self.filesystem.files_in_directory(
            self.tempdir), [
            file1, file2])

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
    self.assertEquals(
        self.filesystem.files_in_directory(
            self.tempdir), [
            file1, file2])

  def test_subdirectories_of_directory_asserts_when_directory_doesnt_exist(
          self):
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
    self.assertEquals(
        self.filesystem.subdirectories_of_directory(
            self.tempdir), [
            dir1, dir2])

  def test_files_in_directory_ignores_subdirectories_by_default(self):
    file1 = os.path.join(self.tempdir, "file1")
    self.touch_file(file1)
    dir1 = os.path.join(self.tempdir, "dir1")
    os.mkdir(dir1)
    file2 = os.path.join(dir1, "file2")
    self.touch_file(file2)

    result = self.filesystem.files_in_directory(self.tempdir)

    self.assertEquals(set(result), set([file1]))

  def test_files_in_directory_should_return_files_in_subdirectories_when_include_subdirectories_is_true(self):
    file1 = os.path.join(self.tempdir, "file1")
    self.touch_file(file1)
    dir1 = os.path.join(self.tempdir, "dir1")
    os.mkdir(dir1)
    file2 = os.path.join(dir1, "file2")
    self.touch_file(file2)

    result = self.filesystem.files_in_directory(self.tempdir, include_subdirectories=True)

    self.assertEquals(set([file1, file2]), set(result))

  def test_subdirectories_of_directory_should_return_subdirectories_of_subdirectories_when_recursive_is_true(self):
    dir1 = os.path.join(self.tempdir, "dir1")
    dir11 = os.path.join(dir1, "dir11")
    dir2 = os.path.join(self.tempdir, "dir2")
    dir21 = os.path.join(dir2, "dir21")
    dirs = [dir1, dir2, dir11, dir21]
    map(os.mkdir, dirs)

    result = self.filesystem.subdirectories_of_directory(self.tempdir, recursive=True)

    self.assertEquals(set(dirs), set(result))

  @parameterized.expand([
    ('/tmp/dir',  '/some/other/dir',  '/tmp/dir/some/other/dir'),
    ('/tmp/dir/', '/some/other/dir',  '/tmp/dir/some/other/dir'),
    ('/tmp/dir',  '/some/other/dir/', '/tmp/dir/some/other/dir'),
    ('/tmp/dir/', '/some/other/dir/', '/tmp/dir/some/other/dir'),
    # Test that it doesn't adjust the path if the path already contains the root
    ('/tmp/dir', '/tmp/dir/random/addition', '/tmp/dir/random/addition')
  ])
  @unittest.skipIf(sys.platform.startswith('win'), "Example test data is Posix specific")
  def test_fake_filesystem_adjusts_path_relative_to_root(self, root, path, expected):
    fs = filesystem.FakeFilesystem(root = root)
    self.assertEqual(fs.adjusted_path(path), expected)
