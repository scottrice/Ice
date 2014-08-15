#!/usr/bin/env python

import sys
import traceback

try:
    from ice.runners import qt_runner

    if __name__ == "__main__":
        runner = qt_runner.QtRunner()
        runner.run(sys.argv)
except Exception:
    sys.stdout = open('stdout.log', 'w')
    sys.stderr = open('stderr.log', 'w')
    traceback.print_exc()
    raw_input()
