# encoding: utf-8
"""
steam_banner_creator_tests.py

Created by Wolfgang on 2018-02-10.
Copyright (c) 2018 Wolfgang Bergbauer. All rights reserved.
"""

import unittest

import os
from mockito import *

# I need to do this instead of importing the class explicitly so that I can
# override the urllib2 function.
# TODO: Use dependency injection so I don't need to use that hack.
from ice.gridproviders import thegamesdb_provider
from ice.steam_banner_creator import SteamBannerCreator


class SteamBannerCreatorTests(unittest.TestCase):

    def test_convertAll(self):
        folder = "D:\\Steam\\userdata\\17910320\\config\\grid\\"
        converter = SteamBannerCreator()
        for filename in os.listdir(folder):
            converter.convertToSteamBannerImage(folder + filename)

    def test_createImage(self):
        testImagePath = "C:\\Users\\bergb\\test.jpg"
        SteamBannerCreator().convertToSteamBannerImage(testImagePath)