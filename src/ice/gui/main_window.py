"""
main_window.py

Created by Scott on 2014-08-14.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

from PyQt4 import QtGui
from ice.gui.tabs.sync_tab_widget import SyncTabWidget
from ice.gui.tabs.consoles_tab_widget import ConsolesTabWidget
from ice.gui.tabs.emulators_tab_widget import EmulatorsTabWidget
from ice.gui.tabs.settings_tab_widget import SettingsTabWidget

class MainWindow(QtGui.QMainWindow):

  def __init__(self):
    super(MainWindow, self).__init__()

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

    self.tabs = {
      "Sync":       SyncTabWidget(),
      "Consoles":   ConsolesTabWidget(),
      "Emulators":  EmulatorsTabWidget(),
      "Settings":   SettingsTabWidget(),
    }

    tab_order = [
      "Sync",
      "Consoles",
      "Emulators",
      "Settings",
    ]

    for tab_name in tab_order:
      widget = self.tabs[tab_name]
      self.tabWidget.addTab(widget, tab_name)
    self.layout.addWidget(self.tabWidget)
