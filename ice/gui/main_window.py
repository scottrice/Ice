"""
main_window.py

Created by Scott on 2014-08-14.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

from PyQt4 import QtGui

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

    self.setGeometry(300, 300, 300, 200)
    self.setWindowTitle('Menubar')    
    self.show()