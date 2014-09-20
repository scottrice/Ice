"""
command_line_runner.py

Created by Scott on 2014-08-14.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

from ice_runner import IceRunner

class CommandLineRunner(object):

  def run(self, argv):
    # TODO: Configure IceRunner based on the contents of argv
    runner = IceRunner()
    runner.run()
    # Keeps the console from closing (until the user hits enter) so they can
    # read any console output
    print ""
    print "Close the window, or hit enter to exit..."
    raw_input()
