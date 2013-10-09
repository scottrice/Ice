#!/usr/bin/env python
# encoding: utf-8
"""
steam_user_manager_tests.py

Created by Scott on 2012-12-26.
Copyright (c) 2012 Scott Rice. All rights reserved.
"""

import os
import unittest

import steam_installation_location_manager
from steam_user_manager import *

class SteamUserManagerTests(unittest.TestCase):
    def setUp(self):
        self.steam_name = "meris608"
        self.steam_id = 20293187
        self.community_id_32 = 40586375
        self.community_id_64 = 76561198000852103
    
    def test_community_id_64_from_name(self):
	    self.assertEqual(communityid64_from_name(self.steam_name),self.community_id_64)
	
    def test_steam_id_from_name(self):
        self.assertEqual(steam_id_from_name(self.steam_name),self.steam_id)
	
    def test_community_id_32_from_name(self):
        self.assertEqual(communityid32_from_name(self.steam_name),self.community_id_32)
	
    def test_name_from_communityid64(self):
        self.assertEqual(name_from_communityid64(self.community_id_64),self.steam_name)
    
    def test_name_from_communityid32(self):
        self.assertEqual(name_from_communityid32(self.community_id_32),self.steam_name)
        
    def test_userdata_directory_for_name(self):
        """
        The userdata directory for a name should be the same directory as it is
        for the 32 bit community id associated with the name
        """
        self.assertEqual(userdata_directory_for_name(self.steam_name),userdata_directory_for_user_id(self.community_id_32))
        
    def test_userdata_directory_for_user_id(self):
        """
        The userdata directory for a user_id should be in the userdata 
        directory for the given Steam installation, and the directory should
        be named the same as the user id
        """
        ud_dir = userdata_directory_for_user_id(self.community_id_32)
        # dirname removes the trailing /, which I keep in 
        # steam_userdata_location, so I add that back on for the equality check
        self.assertEqual(os.path.dirname(ud_dir)+os.sep,steam_installation_location_manager.steam_userdata_location())
        self.assertEqual(int(os.path.basename(ud_dir)),self.community_id_32)
        
        
    def test_shortcuts_file_for_user_id(self):
        """
        The shortcuts file for a given user id should be the result of the
        userdata_directory_for_user_id method, with 'config/shortcuts.vdf'
        added on
        """
        my_shortcuts_file = shortcuts_file_for_user_id(self.community_id_32)
        config_dir = os.path.join(userdata_directory_for_user_id(self.community_id_32),"config")
        self.assertEqual(os.path.dirname(my_shortcuts_file),config_dir)
        self.assertEqual(os.path.basename(my_shortcuts_file),"shortcuts.vdf")
        
    def test_user_ids_on_this_machine(self):
        """
        Finds a list of user_ids that have folders defined on this machine.
        There is no requirement that they have an existing shortcuts.vdf file,
        just that they have a folder named after their user id on the userdata
        folder
        """
        # I am going to test this by getting the list of people defined on the
        # current machine (the one running the tests), adding another folder
        # with an arbitrary id, making sure the new results are the old results
        # plus the arbitrary id, and then removing the new id
        existing_ids = user_ids_on_this_machine()
        # 1 is not a valid 32 bit community id, but we dont care about
        # validity, we just want to know that it correctly reads from the
        # directory.
        os.mkdir(userdata_directory_for_user_id(1))
        updated_ids = user_ids_on_this_machine()
        expected_ids = existing_ids
        expected_ids.append(1)
        os.rmdir(userdata_directory_for_user_id(1))
        # We don't care about order, so we convert to a set first, and make
        # sure that updated_ids = existing_ids + 1
        self.assertEqual(set(expected_ids),set(updated_ids))
        