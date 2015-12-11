# encoding: utf-8
"""
local_provider_tests.py

Created by Scott on 2014-08-18.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

import unittest
from mockito import *

from ice.gridproviders.combined_provider import CombinedProvider


class CombinedProviderTests(unittest.TestCase):

  def test_is_enabled_returns_false_when_no_providers_are_enabled(self):
    provider1 = mock()
    when(provider1).is_enabled().thenReturn(False)

    provider2 = mock()
    when(provider2).is_enabled().thenReturn(False)

    combined_provider = CombinedProvider(provider1, provider2)
    self.assertFalse(combined_provider.is_enabled())

  def test_is_enabled_returns_true_if_at_least_one_provider_is_enabled(self):
    provider1 = mock()
    when(provider1).is_enabled().thenReturn(False)

    provider2 = mock()
    when(provider2).is_enabled().thenReturn(True)

    combined_provider = CombinedProvider(provider1, provider2)
    self.assertTrue(combined_provider.is_enabled())

  def test_image_for_rom_returns_image_from_earlier_provider_first(self):
    rom = mock()

    image1 = mock()
    provider1 = mock()
    when(provider1).is_enabled().thenReturn(True)
    when(provider1).image_for_rom(rom).thenReturn(image1)

    image2 = mock()
    provider2 = mock()
    when(provider2).is_enabled().thenReturn(True)
    when(provider2).image_for_rom(rom).thenReturn(image2)

    combined_provider = CombinedProvider(provider1, provider2)
    self.assertEquals(combined_provider.image_for_rom(rom), image1)

  def test_image_for_rom_returns_image_from_later_provider_when_first_returns_none(self):
    rom = mock()

    provider1 = mock()
    when(provider1).is_enabled().thenReturn(True)
    when(provider1).image_for_rom(rom).thenReturn(None)

    image2 = mock()
    provider2 = mock()
    when(provider2).is_enabled().thenReturn(True)
    when(provider2).image_for_rom(rom).thenReturn(image2)

    image3 = mock()
    provider3 = mock()
    when(provider3).is_enabled().thenReturn(True)
    when(provider3).image_for_rom(rom).thenReturn(image3)

    combined_provider = CombinedProvider(provider1, provider2, provider3)
    self.assertEquals(combined_provider.image_for_rom(rom), image2)

  def test_image_for_rom_skips_disabled_providers(self):
    rom = mock()

    image1 = mock()
    provider1 = mock()
    when(provider1).is_enabled().thenReturn(False)
    when(provider1).image_for_rom(rom).thenReturn(image1)

    image2 = mock()
    provider2 = mock()
    when(provider2).is_enabled().thenReturn(True)
    when(provider2).image_for_rom(rom).thenReturn(image2)

    combined_provider = CombinedProvider(provider1, provider2)
    self.assertEquals(combined_provider.image_for_rom(rom), image2)
