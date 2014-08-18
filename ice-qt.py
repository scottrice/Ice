#!/usr/bin/env python

import sys
import traceback

try:
    from ice.runners import qt_runner

    if __name__ == "__main__":
        runner = qt_runner.QtRunner()
        runner.run(sys.argv)
except Exception:
    stderr = sys.stderr
    with open('stderr.log', 'w') as f:
      sys.stderr = f
      traceback.print_exc()
      sys.stderr = stderr
    print "A fatal error occurred. Check `stderr.log` for more details"
    raw_input()
