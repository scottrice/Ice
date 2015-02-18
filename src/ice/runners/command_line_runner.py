"""
command_line_runner.py

Created by Scott on 2014-08-14.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

from __future__ import print_function
from ice.runners.ice_engine import IceEngine


class CommandLineRunner(object):

  def run(self, argv):
    # TODO: Configure IceEngine based on the contents of argv
    engine = IceEngine()
    engine.run()
    # Keeps the console from closing (until the user hits enter) so they can
    # read any console output
    print("")
    print("Close the window, or hit enter to exit...")
    try: raw_input()
    except NameError: input()
