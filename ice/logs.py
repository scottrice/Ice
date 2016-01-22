# encoding: utf-8
"""
IceLogging.py

Created by Scott on 2013-01-24.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os
import time
import traceback

import logging
import logging.handlers

import paths

class IceLevelTagFilter(logging.Formatter):

  def _tag_for_level(self, levelno):
    name = logging.getLevelName(levelno)
    return "" if levelno is logging.INFO else "[%s] " % name

  def filter(self, record):
    record.leveltag = self._tag_for_level(record.levelno)
    return True

def create_logger():
    # steam handler (only print info messages to terminal)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.addFilter(IceLevelTagFilter())
    ch.setFormatter(logging.Formatter('%(leveltag)s%(message)s'))

    # logfile handler (print all messages to logfile)
    # - max file size of 1mb
    # - log file is stored in `log_file_location` (which is inside application_data_dir)
    fh = logging.handlers.RotatingFileHandler(
        filename=paths.log_file_location(),
        maxBytes=1048576,
        backupCount=5)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(
        logging.Formatter('%(asctime)s [%(levelname)s][%(filename)s][%(funcName)s:%(lineno)s]: %(message)s'))

    # loggers
    logger = logging.getLogger('Ice')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

logger = create_logger()
