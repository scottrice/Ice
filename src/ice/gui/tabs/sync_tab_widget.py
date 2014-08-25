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
    self.initSyncButton(layout)
    self.initPreview(layout)
    self.setLayout(layout)

  def initSyncButton(self, layout):
    hbox = QtGui.QHBoxLayout()
    button = QtGui.QPushButton("Sync ROMs", self)
    hbox.addStretch(1)
    hbox.addWidget(button)
    hbox.addStretch(1)
    layout.addLayout(hbox)

    self.syncButton = button

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
    # self.clearPreview()
    # for rom in roms:
    #   self.addROM(rom)

  def addROM(self, rom):
    pass
