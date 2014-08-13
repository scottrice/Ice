#!/usr/bin/env python
# encoding: utf-8
"""
process_helper.py

Created by Scott on 2013-06-03.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import psutil

def steam_is_running():
  for pid in psutil.pids():
    try:
      p = psutil.Process(pid)
      if p.name().lower().startswith('steam'):
        return True
    except Exception:
      continue
  return False
