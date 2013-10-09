#!/usr/bin/env python
# encoding: utf-8
"""
steam_user_manager.py

Created by Scott on 2012-12-23.
Copyright (c) 2012 Scott Rice. All rights reserved.

The purpose of this class is to handle anything related to Steam user accounts
A big part of that is abstracting away the conversion between Steam usernames
and Steam IDs. It should also be able to determine the path to the userdata 
folder for a given user (finding the directory containing all of the different
userdata folders should be the job of the steam_installation_location_manager) 

Functionality should be added to this module if two conditions are met. The
first is if it is related at all to Steam User accounts, and the second is if
it doesn't involve Ice in any way. If there is functionality related to Steam
Users, but it involves Ice, it should most likely go in the filesystem_helper
(as the filesystem is a big reason Ice needs to know about Steam users)
"""

import os

import httplib

import steam_installation_location_manager

name_to_id_cache = {}
id_to_name_cache = {}

###############################################################################
# Most of the information used in the following 4 methods I obtained via this
# super helpful documentation page. Thank you Valve!
# https://developer.valvesoftware.com/wiki/SteamID
###############################################################################

# This is the V value that is used for individuals. Since we are only 
# converting things for users, we can just hard code it
__v_value__ = 0x0110000100000000

def communityid64_from_name(username):
    """
    The 64 bit id can be retrieved by making a request to the following URL
    http://steamcommunity.com/id/{name}?xml=1
    
    This returns XML, with the 64bit Steam Community ID as an element.
    
    This method also caches the value for a user, so I don't hit the network
    like 8 times trying to do something simple
    """
    if username not in name_to_id_cache:
        # Sometimes Steam will randomly give me a 503 service unavailable.
        # Keep attempting to reach Steam until it gives me a 200
        while True:
            conn = httplib.HTTPConnection("steamcommunity.com")
            url = "/id/%s?xml=1" %  username
            conn.request("GET",url)
            response = conn.getresponse()
            if response.status != 503:
                break
        xml_string = response.read()
        # Rather than parse the XML (which has the possibility of being quite slow,
        # along with adding a dependency on an XML parser), I will instead just do
        # some simple string searching to find the open and close tags for the
        # steamID64 element.
        id_start = xml_string.find("<steamID64>") + len("<steamID64>")
        id_end = xml_string.find("</steamID64>")
        name_to_id_cache[username] = int(xml_string[id_start:id_end])
    return name_to_id_cache[username]

def __y_value__(username):
    """
    Y is either 0 or 1 based on whether the 64 bit community id is even or odd.
    According to the documentation, if W is even then Y is 1, if W is odd Y is
    0. This is the same as doing a binary AND operation between W and 1
    """
    return communityid64_from_name(username) & 1

def steam_id_from_name(username):
    """
    Reverse engineering the Steam ID of a user revolves around the formula
    W = Z * 2 + V + Y, where
    W = The 64 bit Community ID for the user
    Z = The Steam User ID
    V = The 64 bit Steam Account Type Identifier (0x0110000100000000 for users)
    Y = Either 0 or 1, can be determined based on whether W is even or odd
    
    Doing some arithmatic, the formula turns in to Z = (W - V - Y) / 2
    
    Returns Z from the above formula
    """
    w = communityid64_from_name(username)
    v = __v_value__
    y = __y_value__(username)
    z = (w - v - y) / 2
    return z

def communityid32_from_name(username):
    """
    Calculated based on the formula W = Z * 2 + Y where
    W = The 32 bit Community ID for the user
    Z = The Steam ID for the user
    Y = 1 or 0 based on whether W is even or odd
    """
    z = steam_id_from_name(username)
    y = __y_value__(username)
    return (z * 2) + y
    
def name_from_communityid32(user_id):
    w = user_id
    y = w & 1
    z = (w - y) / 2
    v = __v_value__
    return name_from_communityid64((z * 2) + v + y)

def name_from_communityid64(user_id):
    """
    Makes a request to http://steamcommunity.com/profiles/{id64}, which then
    sets the 'location' header variable to the correct location.
    """
    if user_id not in id_to_name_cache:
        while True:
            conn = httplib.HTTPConnection("steamcommunity.com")
            url = "/profiles/%s" % str(user_id)
            conn.request("HEAD",url)
            response = conn.getresponse()
            if response.status != 503:
                break
        # profile_url is of the form "http://steamcommunity.com/id/{username}/"
        profile_url = response.getheader("location")
        # Chop off the beginning of profile url, such that only the name remains
        # The 29 should chop off http://steamcommunity.com/id/ and the -1 should
        # chop off the trailing /
        id_to_name_cache[user_id] = profile_url[29:-1]
    return id_to_name_cache[user_id]

def userdata_directory_for_name(username):
    """
    The userdata directory uses the 32 bit community id as a unique identifier
    for the folders. This function uses that fact and returns the folder by
    converting the name into a 32 bit community id, and then using the
    userdata_directory_for_user_id function to return the directory
    """
    return userdata_directory_for_user_id(communityid32_from_name(username))

def userdata_directory_for_user_id(user_id):
    """
    Returns the path to the userdata directory for a specific user
    
    The userdata directory is where Steam keeps information specific to certain
    users. Of special note for Ice is the config/shortcuts.vdf file, which
    contains all of the 'Non-Steam Games' shortcuts.
    """
    return os.path.join(steam_installation_location_manager.steam_userdata_location(),str(user_id))
    
def shortcuts_file_for_user_id(user_id):
    """
    Returns the path to the shortcuts.vdf file for a specific user
    
    This is really just a convenience method, as it just calls
    userdata_directory_for_user_id, and then adds the path element
    /config/shortcuts.vdf to the result
    """
    return os.path.join(os.path.join(userdata_directory_for_user_id(user_id),"config"),"shortcuts.vdf")
    
def user_ids_on_this_machine():
    """
    Reads the userdata folder to find a list of IDs of Users on this machine.
    This function returns the user_ids in the communityid32 format, so use
    those related methods to convert to other formats
    
    The userdata folder contains a bunch of directories that are all 32 bit
    community ids, so to find a list of ids on the machine we simply find a
    list of subfolders inside the userdata folder
    """
    ids = []
    userdata_dir = steam_installation_location_manager.steam_userdata_location()
    for entry in os.listdir(userdata_dir):
        if os.path.isdir(os.path.join(userdata_dir,entry)):
            ids.append(int(entry))
    return ids