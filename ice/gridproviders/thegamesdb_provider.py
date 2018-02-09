#!/usr/bin/env python
# encoding: utf-8
"""
thegamesdb_provider.py
Created by Wolfgang Bergbauer on 2018-02-09.
Copyright (c) 2018 Wolfgang Bergbauer. All rights reserved.
"""
import requests

import xml.etree.ElementTree

import shutil

import grid_image_provider

from ice.logs import logger


class TheGamesDBProvider(grid_image_provider.GridImageProvider):

    @staticmethod
    def user_agent():
        return "Mozilla/5.0"

    @staticmethod
    def api_url_findId():
        return "http://thegamesdb.net/api/GetGamesList.php?name="

    @staticmethod
    def api_url_getArt():
        return "http://thegamesdb.net/api/GetArt.php?id="

    def http_get(self, url):
        return requests.get(url, {'User-agent': self.user_agent()})

    def searchTheGamesDb(self, rom):
        url = self.api_url_findId() + str(rom.name)
        try:
            response = self.http_get(url)
            body = response.content
            gameList = xml.etree.ElementTree.fromstring(body)
            foundImage = self.findImageForPlattformGame(gameList, rom)
            return foundImage
        except IOError as error:
            logger.debug(
                "There was an error contacting %s" % url
            )

    def getFileType(self, url):
        return url[-4:]

    def download_image(self, url):

        filetype = self.getFileType(url)
        logger.debug(
            "Downloading %s \n Extrated filetype: %s " % (url, filetype)
        )
        if filetype is not None and len(filetype) > 3:

            from tempfile import mkstemp
            fd, path = mkstemp(suffix=filetype)
            response = requests.get(url, stream=True)
            with open(path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            return path

    def findArtWorkUrl(self, gameId):
        url = self.api_url_getArt() + str(gameId)
        try:
            response = self.http_get(url)
            body = response.content
            xmlResult = xml.etree.ElementTree.fromstring(body)
            baseImgUrl = xmlResult._children[0].text
            imagesXml = xmlResult._children[1]
            imgUrl = None

            # try to find a fanart
            boxarts = imagesXml.findall("boxart")
            frontBoxArt = self.findFrontBoxArt(boxarts)

            if frontBoxArt is not None:
                imgUrl = frontBoxArt.text
            else:
                fanart = imagesXml.find("fanart")
                if fanart is not None:
                    imgUrl = fanart.text
                else:
                    if len(imagesXml._children) > 0:
                        # take any image which is available
                        imgUrl = imagesXml._children[0].text

            if imgUrl is not None:
                return baseImgUrl + imgUrl
            else:
                return None
        except IOError as error:
            logger.debug(
                "There was an error contacting %s" % url
            )

    def image_for_rom(self, rom):
        imgUrl = self.searchTheGamesDb(rom)
        if imgUrl is not None:
            return self.download_image(imgUrl)

    def findFrontBoxArt(self, boxarts):
        if boxarts is not None:
            for boxart in boxarts:
                if boxart.get('side') == "front":
                    return boxart

    def findImageForPlattformGame(self, gameList, rom):
        romConsole = rom.console.fullname
        foundgame = None
        foundImage = None
        for game in gameList:
            gameConsole = game.find('Platform').text
            if gameConsole == romConsole or gameConsole in romConsole or romConsole in gameConsole:
                foundImage = self.findArtWorkUrl(game.find('id').text)
                if foundImage is not None:
                    foundgame = game
                    break

        # If no suitable console was found, take the first one
        if foundgame is None and len(gameList._children) > 0:
            foundgame = gameList._children[0]
            foundImage = self.findArtWorkUrl(foundgame.find('id').text)

        return foundImage
