"""
sync_tab.py

Created by Yale Thomas on 8-18-2014
"""

from PyQt4 import QtGui

from ice.gui.steam_preview_widget import SteamPreviewWidget

class SyncTabWidget(QtGui.QWidget):

  def __init__(self):
    super(SyncTabWidget, self).__init__()
    self.userChangedCallback = None

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

    userDropdown = QtGui.QComboBox()
    userDropdown.currentIndexChanged.connect(self.onDropdownIndexChanged)

    rightbox.addStretch(1)
    rightbox.addWidget(QtGui.QLabel("User: "))
    rightbox.addWidget(userDropdown)

    hbox.addLayout(leftbox)
    hbox.addWidget(button)
    hbox.addLayout(rightbox)

    layout.addLayout(hbox)

    self.syncButton = button
    self.userDropdown = userDropdown

  def initPreview(self, layout):
    self.previewWidget = SteamPreviewWidget()
    layout.addWidget(self.previewWidget)

  def onDropdownIndexChanged(self):
    print "onDropdownIndexChanged"
    if self.userChangedCallback is not None:
      self.userChangedCallback(self.selectedUserIndex())

  def selectedUserIndex(self):
    return self.userDropdown.currentIndex()

  def populateUsersDropdownWithUsers(self, users):
    self.userDropdown.clear()
    for user in users:
      self.userDropdown.addItem(str(user.id32))
    self.userDropdown.setCurrentIndex(0)

  def setPreviewForUser(self, user):
    self.previewWidget.setUser(user)

  def setUserChangedCallback(self, callback):
    self.userChangedCallback = callback

  def setOnSyncCallback(self, callback):
    self.syncButton.clicked.connect(callback)

  def setROMs(self, roms):
    self.previewWidget.setROMs(roms)

  def addROM(self, rom):
    pass
