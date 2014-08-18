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
import settings

import logging
import logging.handlers

class IceLogger():
    ''' initialize our loggers '''
    def __init__(self):
        # steam handler (only print info messages to terminal)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter('%(asctime)s (%(name)s) %(levelname)s: %(message)s'))

        # logfile handler (print all messages to logfile)
        # - max file size of 1mb
        # - log file is stored in root ice folder and is named 'ice.log'
        fh = logging.handlers.RotatingFileHandler(filename='ice.log', maxBytes=1048576, backupCount=5)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter('%(asctime)s (%(name)s) %(levelname)s: %(message)s'))

        # loggers
        self.logger = logging.getLogger('ice')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

        self.log        = self.logger.info
        self.debug      = self.logger.debug
        self.warning    = self.logger.warning
        self.error      = self.logger.error

    def exception(self, message="An exception occurred!"):
        self.logger.exception(message)

    # premade logs
    def log_config_error(self, error):
        self.error("There was a problem with '[%s] %s' in %s" % (error.section, error.key, error.file))
        config = settings.settings_for_file(error.file)
        try:
            self.error("The current value is set to '%s'" % config.get(error.section, error.key))
        except KeyError as e:
            self.error(e.message)
        self.error(error.fix_instructions)

    def log_emulator_state(self, emulator):
        if emulator.is_enabled():
          self.log("Detected Emulator: %s" % emulator)
        else:
          self.warning("[DISABLED] Issue detected with emulator `%s`" % emulator)

    def log_console_state(self, console):
        """
        Logs whether a console is enabled or not.
        """
        if console.is_enabled():
          self.log("Detected Console: %s => %s" % (console, console.emulator))
        # TODO: Move this logic into a function on Console which gives a
        # stringified reason why the console is not enabled
        elif console.emulator == None:
          self.warning("[DISABLED] No emulator provided for console `%s`" % console)
        else:
          self.warning("[DISABLED] Issue detected with console `%s`" % console)

    def log_state_of_the_world(self, emulators, consoles):
        for e in emulators:
          self.log_emulator_state(e)
        for c in consoles:
          self.log_console_state(c)


# create our IceLogger object
ice_logger = IceLogger()

