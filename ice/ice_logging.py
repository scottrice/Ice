#!/usr/bin/env python
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

class IceLevelTagFilter(logging.Formatter):

  def _tag_for_level(self, levelno):
    name = logging.getLevelName(levelno)
    return "" if levelno is logging.INFO else "[%s] " % name

  def filter(self, record):
    record.leveltag = self._tag_for_level(record.levelno)
    return True

class IceLogger():

  ''' initialize our loggers '''

  def __init__(self, verbose=False):
    # steam handler (only print info messages to terminal)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO if not verbose else logging.DEBUG)
    ch.addFilter(IceLevelTagFilter())
    ch.setFormatter(logging.Formatter('%(leveltag)s%(message)s'))

    # logfile handler (print all messages to logfile)
    # - max file size of 1mb
    # - log file is stored in root ice folder and is named 'ice.log'
    fh = logging.handlers.RotatingFileHandler(
        filename='ice.log',
        maxBytes=1048576,
        backupCount=5)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(
        logging.Formatter('%(asctime)s [%(levelname)s][%(filename)s][%(funcName)s:%(lineno)s]: %(message)s'))

    # loggers
    self.logger = logging.getLogger('Ice')
    self.logger.setLevel(logging.DEBUG)
    self.logger.addHandler(ch)
    self.logger.addHandler(fh)

    self.info = self.logger.info
    self.debug = self.logger.debug
    self.warning = self.logger.warning
    self.error = self.logger.error
    self.exception = self.logger.exception

  def log_emulator_state(self, emulator):
    if emulator.is_enabled():
      self.info("Detected Emulator: %s" % emulator)
    else:
      self.warning("Issue detected with emulator `%s`" % emulator)

  def log_console_state(self, console):
    """
    Logs whether a console is enabled or not.
    """
    if console.is_enabled():
      self.info("Detected Console: %s => %s" % (console, console.emulator))
    # TODO: Move this logic into a function on Console which gives a
    # stringified reason why the console is not enabled
    elif console.emulator is None:
      self.warning(
          "No emulator provided for console `%s`" %
          console)
    else:
      self.warning("Issue detected with console `%s`" % console)

  def log_configuration(self, config):
    self.debug("Using `config.txt` at `%s`" % config.config_backing_store.path)
    self.debug(
        "Using `consoles.txt` at `%s`" %
        config.console_manager.backing_store.path)
    self.debug(
        "Using `emulators.txt` at `%s`" %
        config.emulator_manager.backing_store.path)
    for emulator in config.emulator_manager:
      self.log_emulator_state(emulator)
    for console in config.console_manager:
      self.log_console_state(console)
