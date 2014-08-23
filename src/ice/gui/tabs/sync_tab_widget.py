"""
sync_tab.py

Created by Yale Thomas on 8-18-2014
"""

from PyQt4 import QtGui

from ice.gui.steam_preview_widget import SteamPreviewWidget

class SyncTabWidget(QtGui.QWidget):

  def __init__(self):
    super(SyncTabWidget, self).__init__()

    layout = QtGui.QVBoxLayout(self)
    syncButton = QtGui.QPushButton("Sync ROMs", self)
    steamPreview = SteamPreviewWidget()
    layout.addWidget(syncButton)
    layout.addWidget(steamPreview)
    self.setLayout(layout)