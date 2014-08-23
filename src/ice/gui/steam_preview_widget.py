"""
steam_preview_widget.py

Created by Scott Rice on 8-22-2014
"""

from PyQt4 import QtGui

class SteamPreviewWidget(QtGui.QWidget):

  def __init__(self):
    super(SteamPreviewWidget, self).__init__()
    header = QtGui.QLabel('Steam Preview')
    header.setFont(QtGui.QFont('SansSerif', 50))

    hbox = QtGui.QHBoxLayout()
    hbox.addStretch(1)
    hbox.addWidget(header)
    hbox.addStretch(1)

    self.setLayout(hbox)
