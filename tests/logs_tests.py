# encoding: utf-8

import os
import shutil
import tempfile
import unittest

from mockito import *

from ice import logs

class LogsTests(unittest.TestCase):
  def setUp(self):
    self.tempdir = tempfile.mkdtemp()
    self.old_log_file_location = logs.paths.log_file_location

  def tearDown(self):
    logs.paths.log_file_location = self.old_log_file_location
    shutil.rmtree(self.tempdir)

  def test_create_logger_creates_directory_containing_log_file_if_it_doesnt_exist(self):
    nonexistant_subdirectory = os.path.join(self.tempdir, "DNE")
    final_path = os.path.join(nonexistant_subdirectory, "ice.log")
    logs.paths.log_file_location = lambda: final_path

    self.assertFalse(os.path.exists(nonexistant_subdirectory))
    new_logger = logs.create_logger()
    self.assertIsNotNone(new_logger)
    self.assertTrue(os.path.exists(nonexistant_subdirectory))
