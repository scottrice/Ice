"""
main_window.py

Created by Scott on 2014-08-14.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

from PyQt4 import QtGui
from ice.gui.tabs.sync_tab_controller import SyncTabController
from ice.gui.tabs.consoles_tab_controller import ConsolesTabController
from ice.gui.tabs.emulators_tab_controller import EmulatorsTabController
from ice.gui.tabs.settings_tab_controller import SettingsTabController
from ice.runners.ice_runner import IceRunner

class MainWindow(QtGui.QMainWindow):

  def __init__(self):
    super(MainWindow, self).__init__()

    self.runner = IceRunner()

    exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
    exitAction.setShortcut('Ctrl+Q')
    exitAction.setStatusTip('Exit application')
    exitAction.triggered.connect(QtGui.qApp.quit)

    self.statusBar()

    menubar = self.menuBar()
    fileMenu = menubar.addMenu('&File')
    fileMenu.addAction(exitAction)

    self.initUI()
    self.initTabs()

    self.show()


  def initUI(self):
    QtGui.QToolTip.setFont(QtGui.QFont('SansSerif',10))
    self.setGeometry(300, 300, 800, 600)
    self.setWindowTitle('Ice')
    self.centralWidget = QtGui.QWidget(self)
    self.layout = QtGui.QVBoxLayout(self.centralWidget)
    self.centralWidget.setLayout(self.layout)
    self.setCentralWidget(self.centralWidget)
    self.layoutHolder = QtGui.QWidget(self)

  def initTabs(self):
    self.toolbarHeight = 50
    self.buttonHeight = 50
    self.buttonWidth = 90

    self.tabWidget = QtGui.QTabWidget()

    self.tab_controllers = {
      "Sync":       SyncTabController(self.runner, self.statusBar()),
      "Consoles":   ConsolesTabController(self.runner.config),
      "Emulators":  EmulatorsTabController(self.runner.config),
      "Settings":   SettingsTabController(self.runner.config),
    }

    tab_order = [
      "Sync",
      "Consoles",
      "Emulators",
      "Settings",
    ]

    for tab_name in tab_order:
      controller = self.tab_controllers[tab_name]
      self.tabWidget.addTab(controller.widget, tab_name)
    self.layout.addWidget(self.tabWidget)
