"""
sync_tab.py

Created by Yale Thomas on 8-18-2014
"""

from PyQt4 import QtGui

class SyncTabWidget(QtGui.QWidget):

  def __init__(self):
    super(SyncTabWidget, self).__init__()

    layout = QtGui.QVBoxLayout(self)
    syncButton = QtGui.QPushButton("Sync ROMs", self)
    layout.addWidget(syncButton)
    header = QtGui.QLabel('Sync')
    header.setFont(QtGui.QFont('SansSerif', 50))
    layout.addWidget(syncButton)
    layout.addWidget(header)
    self.setLayout(layout)
