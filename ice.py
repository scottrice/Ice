#!/usr/bin/env python

import sys

from ice.runners import *

if __name__ == "__main__":
  runner = command_line_runner.CommandLineRunner()
  runner.run(sys.argv)
