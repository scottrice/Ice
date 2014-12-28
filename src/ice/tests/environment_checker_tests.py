import os
import shutil
import stat
import tempfile
import unittest

from ice.environment_checker import EnvironmentChecker
from ice.error.env_checker_error import EnvCheckerError


class EnvironmentCheckerTests(unittest.TestCase):

  def setUp(self):
    self.tempdir = tempfile.mkdtemp()

  def tearDown(self):
    shutil.rmtree(self.tempdir)

  def testRequireDirectoryExistsSucceedsWhenDirectoryExists(self):
    try:
      with EnvironmentChecker() as env_checker:
        env_checker.require_directory_exists(self.tempdir)
    except:
      self.fail("Should succeed when given a directory that exists")

  def testRequireDirectoryExistsCreatesMissingDirectory(self):
    path = os.path.join(self.tempdir, "missing")
    self.assertFalse(os.path.exists(path))
    with EnvironmentChecker() as env_checker:
      env_checker.require_directory_exists(path)
    self.assertTrue(os.path.isdir(path))

  def testRequireDirectoryExistsFailsWhenFileExistsAtPath(self):
    path = os.path.join(self.tempdir, "missing")
    self.assertFalse(os.path.exists(path))
    with open(path, "w+") as f:
      f.write("Batman")
    with self.assertRaises(EnvCheckerError):
      with EnvironmentChecker() as env_checker:
        env_checker.require_directory_exists(path)

  def testRequireDirectoryExistsFailsWhenCantCreateMissingDirectory(self):
    parent_path = os.path.join(self.tempdir, "exists")
    os.mkdir(parent_path)
    os.chmod(parent_path, stat.S_IREAD)
    child_path = os.path.join(parent_path, "dne")
    with self.assertRaises(EnvCheckerError):
      with EnvironmentChecker() as env_checker:
        env_checker.require_directory_exists(child_path)

  def testRequireWritablePathSucceedsWithWritablePath(self):
    # Temp directories are writable by default
    try:
      with EnvironmentChecker() as env_checker:
        env_checker.require_writable_path(self.tempdir)
    except:
      self.fail("Should succeed when given a writable path")

  def testRequireWritablePathFailsWhenDirectoryDoesntExist(self):
    path = os.path.join(self.tempdir, "dne")
    with self.assertRaises(EnvCheckerError):
      with EnvironmentChecker() as env_checker:
        env_checker.require_writable_path(path)

  def testRequireWritablePathFailsWhenDirectoryIsntWritable(self):
    path = os.path.join(self.tempdir, "readonly")
    os.mkdir(path)
    os.chmod(path, stat.S_IREAD)
    with self.assertRaises(EnvCheckerError):
      with EnvironmentChecker() as env_checker:
        env_checker.require_writable_path(path)

  def testRequireWritablePathFailsWhenFileIsntWritable(self):
    path = os.path.join(self.tempdir, "mad-scientist")
    with open(path, "w+") as f:
      f.write("its so cool!")
    os.chmod(path, stat.S_IREAD)
    with self.assertRaises(EnvCheckerError):
      with EnvironmentChecker() as env_checker:
        env_checker.require_writable_path(path)

  def testRequireProgramNotRunningFailsWhenProgramIsRunning(self):
    # ASSUMPTION: Since I am writing this in Python I am going to cheat a
    # a little and test this by requiring that `python` is not running. If
    # this test is run by a process whose name is something other than `python`
    # it will fail.
    #
    # Also I should make sure not to make it automatically resolve the error
    # by killing the process
    #
    # That would be bad
    with self.assertRaises(EnvCheckerError):
      with EnvironmentChecker() as env_checker:
        env_checker.require_program_not_running("python")
