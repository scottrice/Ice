#!/usr/bin/env python
# encoding: utf-8
"""
process_helper.py

Created by Scott on 2013-06-03.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import psutil

def steam_is_running():
  return True in [ psutil.Process(pid).name().lower().startswith('steam') for pid in psutil.pids() ]