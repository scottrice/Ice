"""
command_line_runner.py

Created by Scott on 2014-08-14.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

import argparse

from pysteam.steam import get_steam

from ice_engine import IceEngine

from ice import debug
from ice.filesystem import RealFilesystem

class CommandLineRunner(object):

  def __init__(self, steam=None, filesystem=None):
    self.steam = steam if steam is not None else get_steam()
    self.filesystem = RealFilesystem() if filesystem is None else filesystem

  def get_command_line_args(self, argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('pdebug', type=bool, nargs='?', help="Pastes debug logs to pastebin to include with bug reports.")
    parser.add_argument('-c', '--config', type=str, default=None)
    parser.add_argument('-C', '--consoles', type=str, default=None)
    parser.add_argument('-e', '--emulators', type=str, default=None)
    # Debugging options
    parser.add_argument('-d', '--dry-run', action='store_true')
    return parser.parse_args(argv)

  def run(self, argv):
    options = self.get_command_line_args(argv[1:])

    if options.pdebug is True:
      debug.paste_debug_logs()
      return

    engine = IceEngine(self.steam, filesystem = self.filesystem, options = options)
    engine.main(dry_run=options.dry_run)
