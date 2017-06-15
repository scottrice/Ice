#!/usr/bin/env python
# encoding: utf-8
"""
retrogamingcloud_provider.py

Created by W on 2017-06-13.
Copyright (c) 2017 W Anders. All rights reserved.
"""

import sys
import os
import urllib
import json

import grid_image_provider

from ice.logs import logger

class RetroGamingCloudProvider(grid_image_provider.GridImageProvider):

	@staticmethod
	def is_enabled():
		return True

	@staticmethod
	def api_url():
		return "http://retrogaming.cloud/api/v1/game"

	def download_image(self, url):
		(path, headers) = urllib.urlretrieve(url)
		return path

	def rgc_get_result(self, url):
		try:
			response = urllib.urlopen(url)
			return json.loads(response.read())["results"]
		except IOError as error:
			logger.debug(
				"There was an error contacting Retrogaming.cloud"
			)
			return None

	def rgc_search(self, rom):
		api_root = self.api_url()
		url = "%s?name=\"%s\"" % (api_root, rom.name)
		return self.rgc_get_result(url)

	def rgc_get_media(self, game_id):
		api_root = self.api_url()
		url = "%s/%s/media" % (api_root, game_id)
		return self.rgc_get_result(url)

	def image_for_rom(self, rom):
		game_results = self.rgc_search(rom)
		game_by_console = [game for game in game_results if game["platform"]["key"] == rom.console.shortname]
		game_verify_by_name = next((game for game in game_by_console if game["name"] == rom.name), None)
		if game_verify_by_name is None:
			return None
		game_id = game_verify_by_name["id"]
		game_media = self.rgc_get_media(game_id)
		game_grid_url = next((grid["url"] for grid in game_media), None)
		if game_grid_url is None:
			return None
		return self.download_image(game_grid_url)