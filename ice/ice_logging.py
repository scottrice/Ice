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
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter('%(asctime)s (%(name)s) %(levelname)s: %(message)s'))

        # loggers
        self.logger = logging.getLogger('ice')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

    def log(self, message):
        self.logger.info(message)

    def log_debug(self, message):
        self.logger.debug(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    # premade logs
    def log_config_error(self, error):
        self.logger.error("There was a problem with '[%s] %s' in %s" % (error.section, error.key, error.file))
        config = settings.settings_for_file(error.file)
        try:
            self.logger.error("The current value is set to '%s'" % config[error.section][error.key.lower()])
        except KeyError as e:
            if e.message == error.section:
                self.logger.error("No section found named '[%s]'" % e.message)
            else:
                self.logger.error("The key '%s' is missing" % e.message)
        self.logger.error(error.fix_instructions)

    def log_exception(self):
        self.logger.error(traceback.format_exc())



# create our IceLogger object
ice_logger = IceLogger()

def log_file_path():
    """Directory to store the log file"""
    """!! NOT USED IN IceLogger()!! - remove?"""
    # http://stackoverflow.com/questions/279237/python-import-a-module-from-a-folder
    current_directory = os.path.dirname(sys.modules['__main__'].__file__)
    return os.path.join(current_directory,"log.txt")
