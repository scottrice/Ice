"""
command_line_runner.py

Created by Scott on 2014-08-14.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

import argparse

from ice_engine import IceEngine


class CommandLineRunner(object):

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
    engine = IceEngine(options)
    engine.run(dry_run=options.dry_run)
    # Keeps the console from closing (until the user hits enter) so they can
    # read any console output
    print ""
    print "Close the window, or hit enter to exit..."
    raw_input()
