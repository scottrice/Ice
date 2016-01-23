
import os
import tempfile
import unittest

from mockito import *
from nose_parameterized import parameterized

from ice import filesystem
from ice.persistence.adapters import emulator_adapter
from ice import model

class EmulatorAdapterTests(unittest.TestCase):

  def setUp(self):
    fs = filesystem.RealFilesystem()
    self.adapter = emulator_adapter.EmulatorBackedObjectAdapter(fs)

  def test_verify_returns_false_when_location_is_none(self):
    emu = model.Emulator("Mednafen", None, "%l %r")
    self.assertFalse(self.adapter.verify(emu))

  def test_verify_returns_false_when_location_is_empty_string(self):
    emu = model.Emulator("Mednafen", "", "%l %r")
    self.assertFalse(self.adapter.verify(emu))

  def test_verify_returns_true_when_location_doesnt_exist(self):
    emu = model.Emulator("Mednafen", "/some/random/path/that/doesnt/exist", "%l %r")
    self.assertTrue(self.adapter.verify(emu))

  def test_verify_returns_true_when_location_is_directory(self):
    d = tempfile.mkdtemp()
    emu = model.Emulator("Mednafen", d, "%l %r")
    self.assertTrue(self.adapter.verify(emu))
    os.rmdir(d)

  def test_verify_returns_true_when_location_is_file(self):
    (f, path) = tempfile.mkstemp()
    emu = model.Emulator("Mednafen", path, "%l %r")
    self.assertTrue(self.adapter.verify(emu))
    os.remove(path)
