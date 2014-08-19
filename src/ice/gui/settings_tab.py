"""
settings_tab.py

Created by Yale Thomas on 8-18-2014
"""

from PyQt4 import QtGui

class SettingsTab(QtGui.QWidget):

  def __init__(self):
    super(SettingsTab, self).__init__()

    self.layout = QtGui.QGridLayout(self)
    self.setLayout(self.layout)
    font = QtGui.QFont('SansSerif', 50)
    header = QtGui.QLabel('Settings')
    header.setFont(font)
    self.layout.addWidget(header, 1, 5)

  def getWidget(self):
    return self

