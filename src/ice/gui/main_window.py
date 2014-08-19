"""
main_window.py

Created by Scott on 2014-08-14.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

from PyQt4 import QtGui
from ice.gui.sync_tab import SyncTab
from ice.gui.consoles_tab import ConsolesTab
from ice.gui.emulators_tab import EmulatorsTab
from ice.gui.settings_tab import SettingsTab

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

    self.tab_widget = QtGui.QTabWidget()

    self.syncTab = SyncTab()
    self.tab_widget.addTab(self.syncTab.getWidget(), 'Sync')
    self.layout.addWidget(self.tab_widget)

    self.consolesTab = ConsolesTab()
    self.tab_widget.addTab(self.consolesTab.getWidget(), 'Console')
    self.layout.addWidget(self.tab_widget)

    self.emulatorsTab = EmulatorsTab()
    self.tab_widget.addTab(self.emulatorsTab.getWidget(), 'Emulators')
    self.layout.addWidget(self.tab_widget)

    self.settingsTab = SettingsTab()
    self.tab_widget.addTab(self.settingsTab.getWidget(), 'Settings')
    self.layout.addWidget(self.tab_widget)
