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

class ColoredFilter():
    # Explanation: http://en.wikipedia.org/wiki/ANSI_escape_code#Colors
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
    # Explanation: http://en.wikipedia.org/wiki/ANSI_escape_code#CSI_codes
    RESET_SEQ = "\033[0m"
    COLOR_SEQ = "\033[%dm"
    EXT_COLOR_SEQ = "\033[48;5;%dm"

    def __init__(self):
      self.colors = {}

    def levelSequence(self, level):
      return self.colors[level] if level in self.colors else self.RESET_SEQ

    def setColor(self, level, color):
      self.colors[level] = self.COLOR_SEQ % (40 + color)

    def setExtendedColor(self, level, code):
      self.colors[level] = self.EXT_COLOR_SEQ % code

    def filter(self, record):
      record.color = self.levelSequence(record.levelno)
      record.nocolor = self.RESET_SEQ
      return True

class IceLogger():
    ''' initialize our loggers '''
    def __init__(self):
        colorer = ColoredFilter()
        colorer.setColor(logging.ERROR, ColoredFilter.RED)
        colorer.setExtendedColor(logging.WARNING, 94)
        # steam handler (only print info messages to terminal)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.addFilter(colorer)
        ch.setFormatter(logging.Formatter('%(color)s%(levelname)s\t%(nocolor)s %(message)s'))

        # logfile handler (print all messages to logfile)
        # - max file size of 1mb
        # - log file is stored in root ice folder and is named 'ice.log'
        fh = logging.handlers.RotatingFileHandler(filename='ice.log', maxBytes=1048576, backupCount=5)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter('%(asctime)s (%(name)s) %(levelname)s: %(message)s'))

        # loggers
        self.logger = logging.getLogger('Ice')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

        self.info       = self.logger.info
        self.debug      = self.logger.debug
        self.warning    = self.logger.warning
        self.error      = self.logger.error
        self.exception  = self.logger.exception

    def log_emulator_state(self, emulator):
        if emulator.is_enabled():
          self.info("Detected Emulator: %s" % emulator)
        else:
          self.warning("[DISABLED] Issue detected with emulator `%s`" % emulator)

    def log_console_state(self, console):
        """
        Logs whether a console is enabled or not.
        """
        if console.is_enabled():
          self.info("Detected Console: %s => %s" % (console, console.emulator))
        # TODO: Move this logic into a function on Console which gives a
        # stringified reason why the console is not enabled
        elif console.emulator == None:
          self.warning("[DISABLED] No emulator provided for console `%s`" % console)
        else:
          self.warning("[DISABLED] Issue detected with console `%s`" % console)

    def log_configuration(self, config):
        self.debug("Using `config.txt` at `%s`" % config.config_backing_store.path)
        self.debug("Using `consoles.txt` at `%s`" % config.console_manager.backing_store.path)
        self.debug("Using `emulators.txt` at `%s`" % config.emulator_manager.backing_store.path)
        for emulator in config.emulator_manager:
          self.log_emulator_state(emulator)
        for console in config.console_manager:
          self.log_console_state(console)
