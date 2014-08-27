"""
sync_tab.py

Created by Yale Thomas on 8-18-2014
"""

from PyQt4 import QtGui

from ice.gui.steam_preview_widget import SteamPreviewWidget

class SyncTabWidget(QtGui.QWidget):

  def __init__(self, user):
    super(SyncTabWidget, self).__init__()
    self.user = user

    self.initUI()

  def initUI(self):
    layout = QtGui.QVBoxLayout(self)
    self.initTopRow(layout)
    self.initPreview(layout)
    self.setLayout(layout)

  def initTopRow(self, layout):
    hbox = QtGui.QHBoxLayout()
    leftbox = QtGui.QHBoxLayout()
    rightbox = QtGui.QHBoxLayout()

    leftbox.addStretch(1)

    button = QtGui.QPushButton("Sync ROMs", self)

    rightbox.addStretch(1)
    userDropdown = QtGui.QComboBox()
    rightbox.addWidget(QtGui.QLabel("User: "))
    rightbox.addWidget(userDropdown)

    hbox.addLayout(leftbox)
    hbox.addWidget(button)
    hbox.addLayout(rightbox)

    layout.addLayout(hbox)

    self.syncButton = button
    self.userDropdown = userDropdown

  def initPreview(self, layout):
    self.previewWidget = SteamPreviewWidget(self.user)
    layout.addWidget(self.previewWidget)

  def clearPreview(self):
    for index in range(0, self.previewGrid.count()):
      item = self.previewGrid.itemAt(index)
      if item is not None:
        widget = item.widget()
        if widget is not None:
          self.previewGrid.removeWidget(widget)
          widget.deleteLater()

  def setROMs(self, roms):
    self.previewWidget.setROMs(roms)

  def addROM(self, rom):
    pass
