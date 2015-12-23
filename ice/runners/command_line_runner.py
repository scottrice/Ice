"""
command_line_runner.py

Created by Scott on 2014-08-14.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

import argparse

from pysteam.steam import get_steam

from ice_engine import IceEngine


class CommandLineRunner(object):

  def __init__(self, steam=None):
    self.steam = steam if steam is not None else get_steam()

  def get_command_line_args(self, argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=str, default=None)
    parser.add_argument('-C', '--consoles', type=str, default=None)
    parser.add_argument('-e', '--emulators', type=str, default=None)
    # Debugging options
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-d', '--dry-run', action='store_true')
    return parser.parse_args(argv)

  def run(self, argv):
    options = self.get_command_line_args(argv[1:])
    engine = IceEngine(self.steam, options)
    engine.run(dry_run=options.dry_run)
