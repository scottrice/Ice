

import os
import shutil
import tempfile
import unittest

from mockito import *

from nose_parameterized import parameterized

from ice import cache

class CacheTests(unittest.TestCase):

  def setUp(self):
    self.cache = cache.Cache()

  def test_requesting_missing_key_returns_none(self):
    self.assertIsNone(self.cache.get("hero"))

  def test_requesting_cached_key_retuns_cached_value(self):
    self.cache.set("hero", "Iron Man")

    self.assertIsNone(self.cache.get("villain"))
    self.assertEqual(self.cache.get("hero"), "Iron Man")

  def test_requesting_keys_has_no_side_effects(self):
    self.assertIsNone(self.cache.get("a"))
    self.assertIsNone(self.cache.get("a"))
    self.assertIsNone(self.cache.get("a", "b"))
    self.assertIsNone(self.cache.get("a", "b"))
    self.assertIsNone(self.cache.get("a"))

  def test_can_request_multiple_levels_of_key(self):
    self.cache.set("begin", "end", "wtf")

    self.assertEqual(self.cache.get("begin", "end"), "wtf")

  def test_requesting_intermediate_key_returns_another_cache(self):
    self.cache.set("begin", "end", "wtf")

    result = self.cache.get("begin")
    self.assertIsNotNone(result)
    self.assertIsInstance(result, cache.Cache)
    self.assertEqual(result.get("end"), "wtf")

  def test_getting_multiple_level_value_after_setting_intermediate_key_raises(self):
    self.cache.set("a", "b", "some value")

    with self.assertRaises(Exception):
      self.cache.get("a", "b", "c")

  def test_setting_multiple_level_key_overwrites_intermediate_value(self):
    self.cache.set("a", "some value")

    self.assertEqual(self.cache.get("a"), "some value")

    self.cache.set("a", "b", "some other value")

    self.assertIsInstance(self.cache.get("a"), cache.Cache)
    self.assertEqual(self.cache.get("a", "b"),  "some other value")
