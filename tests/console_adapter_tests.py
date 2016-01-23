
import unittest

from mockito import *
from nose_parameterized import parameterized

from ice.persistence.adapters import console_adapter
from ice import model

from testinfra import fixtures

class ConsoleAdapterTests(unittest.TestCase):

  def test_verify(self):
    emu = mock()
    adapter = console_adapter.ConsoleBackedObjectAdapter([])
    valid = model.Console("Nintendo", "NES", "", "", "", "", "", emu)
    self.assertTrue(adapter.verify(valid))

    invalid = model.Console("Nintendo", "NES", "", "", "", "", "", None)
    self.assertFalse(adapter.verify(invalid))
