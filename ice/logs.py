# encoding: utf-8
"""
IceLogging.py

Created by Scott on 2013-01-24.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import inspect
import os
import sys
import time
import traceback

import logging
import logging.handlers

import paths

STREAM_STRING_FORMAT = '%(leveltag)s%(message)s'
FILE_STRING_FORMAT = '%(asctime)s [%(levelname)s][%(filename)s][%(funcName)s:%(lineno)s]: %(message)s'

def is_test_stack_frame(frame):
  # The path of the executing file is in frame[1]
  path = frame[1]
  # See if the path is in the unittest module
  return "unittest" in path

def is_running_in_test():
  current_stack = inspect.stack()
  return any(map(is_test_stack_frame, inspect.stack()))

class IceLevelTagFilter(logging.Formatter):

  def _tag_for_level(self, levelno):
    name = logging.getLevelName(levelno)
    return "" if levelno is logging.INFO else "[%s] " % name

  def filter(self, record):
    record.leveltag = self._tag_for_level(record.levelno)
    return True

def create_stream_handler(level):
  # steam handler (only print info messages to terminal)
  sh = logging.StreamHandler()
  sh.setLevel(level)
  sh.addFilter(IceLevelTagFilter())
  sh.setFormatter(logging.Formatter(STREAM_STRING_FORMAT))
  return sh

def create_file_handler(level):
  path = paths.log_file_location()
  # Since the logger is created so early in Ice's lifecycle (literally one of
  # the first things, since it happens at import time) its possible that the
  # application_data_directory (where the log file is stored) doesnt exist.
  # Create it now
  directory = os.path.dirname(path)
  if not os.path.exists(directory):
    os.makedirs(directory)

  # logfile handler (print all messages to logfile)
  # - max file size of 1mb
  # - log file is stored in `log_file_location` (which is inside application_data_dir)
  fh = logging.handlers.RotatingFileHandler(
      filename=path,
      maxBytes=1048576,
      backupCount=5)
  fh.setLevel(level)
  fh.setFormatter(logging.Formatter(FILE_STRING_FORMAT))
  return fh

def create_logger():
    sh = create_stream_handler(logging.INFO)
    fh = create_file_handler(logging.DEBUG)
    # loggers
    logger = logging.getLogger('Ice')
    logger.setLevel(logging.DEBUG)
    if not is_running_in_test():
      logger.addHandler(sh)
      logger.addHandler(fh)
    return logger

logger = create_logger()
