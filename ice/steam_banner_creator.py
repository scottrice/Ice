# encoding: utf-8
"""
steam_banner_creator.py

Created by Wolfgang on 2018-02-10.
Copyright (c) 2018 Wolfgang Bergbauer. All rights reserved.

This class creates a steam banner image from an given image.
"""
from PIL import Image, ImageFilter

from ice.logs import logger


class SteamBannerCreator():

    @staticmethod
    def STEAM_BANNER_HEIGHT():
        return 215

    @staticmethod
    def STEAM_BANNER_SIZE(): return 460, 215

    def convertToSteamBannerImage(self, oldImagePath):
        try:
            background = self.__createGaussianBackground(oldImagePath)
            foreground = self.resizeToHeight(self.STEAM_BANNER_HEIGHT(), oldImagePath)
            background.paste(foreground, (background.size[0]/2 - foreground.size[0] / 2, 0))
            background.save(oldImagePath)
        except IOError as error:
            logger.debug(
                "There was an error converting the image " + oldImagePath + ": " + error.message
            )

    def __createGaussianBackground(self, oldImagePath):
        background = Image.open(oldImagePath)
        background = background.resize(self.STEAM_BANNER_SIZE(), Image.ANTIALIAS)
        background = background.filter(ImageFilter.GaussianBlur(radius=20))
        return background

    def resizeToHeight(self, height, oldImagePath):
        img = Image.open(oldImagePath)
        hpercent = (height / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, height), Image.ANTIALIAS)
        return img