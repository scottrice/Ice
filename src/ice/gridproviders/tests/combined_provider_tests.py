# encoding: utf-8
"""
local_provider_tests.py

Created by Scott on 2014-08-18.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

import mock
import unittest

from ice.gridproviders.combined_provider import CombinedProvider


class CombinedProviderTests(unittest.TestCase):

  def test_is_enabled_returns_false_when_no_providers_are_enabled(self):
    provider1 = mock.MagicMock()
    provider1.is_enabled.return_value = False

    provider2 = mock.MagicMock()
    provider2.is_enabled.return_value = False

    combined_provider = CombinedProvider(provider1, provider2)
    self.assertFalse(combined_provider.is_enabled())

  def test_is_enabled_returns_true_if_at_least_one_provider_is_enabled(self):
    provider1 = mock.MagicMock()
    provider1.is_enabled.return_value = False

    provider2 = mock.MagicMock()
    provider2.is_enabled.return_value = True

    combined_provider = CombinedProvider(provider1, provider2)
    self.assertTrue(combined_provider.is_enabled())

  def test_image_for_rom_returns_image_from_earlier_provider_first(self):
    image1 = mock.MagicMock()
    provider1 = mock.MagicMock()
    provider1.image_for_rom.return_value = image1

    image2 = mock.MagicMock()
    provider2 = mock.MagicMock()
    provider2.image_for_rom.return_value = image2

    mock_rom = mock.MagicMock()
    combined_provider = CombinedProvider(provider1, provider2)
    self.assertEquals(combined_provider.image_for_rom(mock_rom), image1)

  def test_image_for_rom_returns_image_later_provider_when_first_returns_none(
          self):
    provider1 = mock.MagicMock()
    provider1.image_for_rom.return_value = None

    image2 = mock.MagicMock()
    provider2 = mock.MagicMock()
    provider2.image_for_rom.return_value = image2

    image3 = mock.MagicMock()
    provider3 = mock.MagicMock()
    provider3.image_for_rom.return_value = image3

    mock_rom = mock.MagicMock()
    combined_provider = CombinedProvider(provider1, provider2)
    self.assertEquals(combined_provider.image_for_rom(mock_rom), image2)

  def test_image_for_rom_skips_disabled_providers(self):
    image1 = mock.MagicMock()
    provider1 = mock.MagicMock()
    provider1.is_enabled.return_value = False
    provider1.image_for_rom.return_value = image1

    image2 = mock.MagicMock()
    provider2 = mock.MagicMock()
    provider2.image_for_rom.return_value = image2

    mock_rom = mock.MagicMock()
    combined_provider = CombinedProvider(provider1, provider2)
    self.assertEquals(combined_provider.image_for_rom(mock_rom), image2)
