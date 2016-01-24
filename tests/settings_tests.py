

import os
import shutil
import tempfile
import unittest

from mockito import *

from nose_parameterized import parameterized

from ice.gridproviders.consolegrid_provider import ConsoleGridProvider
from ice.gridproviders.local_provider import LocalProvider

from ice import settings

class SettingsTests(unittest.TestCase):

  def setUp(self):
    pass

  @parameterized.expand([
    ("local", [LocalProvider]),
    ("consolegrid", [ConsoleGridProvider]),
    ("local, consolegrid", [LocalProvider, ConsoleGridProvider]),
    ("consOLEGRId ,      LOcaL ", [ConsoleGridProvider, LocalProvider])
  ])
  def test_image_provider(self, spec, classes):
    config = mock()
    config.provider_spec = spec
    result = settings.image_provider(config)
    self.assertEqual(classes, map(lambda p: p.__class__, result.providers))
