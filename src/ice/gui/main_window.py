"""
main_window.py

Created by Scott on 2014-08-14.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

from PyQt4 import QtGui
import sip

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

  def initTabs(self):
    self.tabs = ['Sync', 'Consoles', 'Emulators', 'Settings']

    self.toolbar = QtGui.QButtonGroup()
    self.toolbar.setExclusive(True)

    self.toolbarHeight = 50
    self.buttonHeight = 50
    self.buttonWidth = 90

    switch = {
        'Sync': self.showSync,
        'Consoles': self.showConsoles,
        'Emulators': self.showEmulators,
        'Settings': self.showSettings
    }
    for index, tabName in enumerate(self.tabs):
        myButton = QtGui.QPushButton(tabName, self)
        myButton.resize(self.buttonWidth, self.buttonHeight)
        myButton.clicked.connect(switch[tabName])
        self.toolbar.addButton(myButton)

    self.resize()

  def resize(self):
    # resize toolbar
    for index, button in enumerate(self.toolbar.buttons()):
        button.move(round(self.width()/7*(index+2)-self.buttonWidth/2), round(self.toolbarHeight/2-self.buttonHeight/2))

  def clearTab(self):
    for i in reversed(range(self.layout.count())):
        self.layout.itemAt(i).widget().deleteLater()

  def showSync(self):
    self.clearTab()
    font = QtGui.QFont('SansSerif', 50)
    header = QtGui.QLabel('Sync', self)
    header.setFont(font)
    header.resize(self.buttonWidth*2, self.buttonHeight*2)
    header.move(self.width()/2-self.buttonWidth, self.height()/2-self.buttonHeight)
    self.layout.addWidget(header)
    self.show()

  def showConsoles(self):
    self.clearTab()
    font = QtGui.QFont('SansSerif', 50)
    header = QtGui.QLabel("Consoles", self)
    header.setFont(font)
    header.resize(self.buttonWidth*2, self.buttonHeight*2)
    header.move(self.width()/2-self.buttonWidth, self.height()/2-self.buttonHeight)
    self.layout.addWidget(header)
    self.show()

  def showEmulators(self):
    self.clearTab()
    font = QtGui.QFont('SansSerif', 50)
    header = QtGui.QLabel("Emulators", self)
    header.setFont(font)
    header.resize(self.buttonWidth*2, self.buttonHeight*2)
    header.move(self.width()/2-self.buttonWidth, self.height()/2-self.buttonHeight)
    self.layout.addWidget(header)
    self.show()

  def showSettings(self):
    self.clearTab()
    font = QtGui.QFont('SansSerif', 50)
    header = QtGui.QLabel("Settings", self)
    header.setFont(font)
    header.resize(self.buttonWidth*2, self.buttonHeight*2)
    header.move(self.width()/2-self.buttonWidth, self.height()/2-self.buttonHeight)
    self.layout.addWidget(header)
    self.show()







