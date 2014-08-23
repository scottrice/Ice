#!/usr/bin/env python

import sys
import traceback

try:
    from ice.runners import qt_runner

    if __name__ == "__main__":
        runner = qt_runner.QtRunner()
        runner.run(sys.argv)
except Exception as e:
    stderr = sys.stderr
    with open('stderr.log', 'w') as f:
      sys.stderr = f
      traceback.print_exc()
      sys.stderr = stderr
    print "A fatal error occured:"
    print "\"%s\"" % e
    print "For a full stack trace, see `stderr.log`"
    raw_input()
