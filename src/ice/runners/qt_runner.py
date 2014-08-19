"""
qt_runner.py

Created by Scott on 2014-08-14.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

import sys
from PyQt4 import QtGui

from ice.gui.main_window import MainWindow

class QtRunner(object):
  def run(self, argv):
    app = QtGui.QApplication(argv)
    mw = MainWindow()
    sys.exit(app.exec_())