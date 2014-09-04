"""
settings_tab.py

Created by Yale Thomas on 8-18-2014
"""

from PyQt4 import QtGui

class SettingsTabWidget(QtGui.QWidget):

  def __init__(self):
    super(SettingsTabWidget, self).__init__()

    self.initUI()

  def initUI(self):
    vbox = QtGui.QVBoxLayout()

    roms_dir_label = QtGui.QLabel("ROMs Directory")
    roms_dir_current = QtGui.QLabel()
    roms_dir_button = QtGui.QPushButton("Change Roms Directory", self)
    roms_dir_explanation = QtGui.QLabel("The path to place the ROMs Directory. If a console doesn't have a specific ROMs directory set, then a folder will be created inside this directory to store the console's ROMs")
    roms_dir_explanation.setStyleSheet("QLabel { color: rgba(0,0,0,140); }")

    backup_dir_label = QtGui.QLabel("Backup Directory")
    backup_dir_current = QtGui.QLabel()
    backup_dir_button = QtGui.QPushButton("Change Backup Directory", self)
    backup_dir_explanation = QtGui.QLabel("The path to store backups of the shortcuts.vdf file. Ice will store a copy of the current shortcuts.vdf file every time before it runs")
    backup_dir_explanation.setStyleSheet("QLabel { color: rgba(0,0,0,140); }")

    userdata_label = QtGui.QLabel("Steam Userdata Location")
    userdata_current = QtGui.QLabel()
    userdata_button = QtGui.QPushButton("Change Userdata Directory", self)
    userdata_explanation = QtGui.QLabel("The location of Steam's userdata directory. If this is blank, Ice will attempt to locate the directory on its own")
    userdata_explanation.setStyleSheet("QLabel { color: rgba(0,0,0,140); }")

    vbox.addWidget(roms_dir_label)
    vbox.addWidget(roms_dir_current)
    vbox.addWidget(roms_dir_button)
    vbox.addWidget(roms_dir_explanation)
    vbox.addWidget(self.getHorizontalSeperator())
    vbox.addWidget(backup_dir_label)
    vbox.addWidget(backup_dir_current)
    vbox.addWidget(backup_dir_button)
    vbox.addWidget(backup_dir_explanation)
    vbox.addWidget(self.getHorizontalSeperator())
    vbox.addWidget(userdata_label)
    vbox.addWidget(userdata_current)
    vbox.addWidget(userdata_button)
    vbox.addWidget(userdata_explanation)
    vbox.addStretch(1)

    self.userdataButton = userdata_button
    self.userdataDirectoryDisplayWidget = userdata_current
    self.backupButton = backup_dir_button
    self.backupDirectoryDisplayWidget = backup_dir_current
    self.romsButton = roms_dir_button
    self.romsDirectoryDisplayWidget = roms_dir_current
    self.setLayout(vbox)

  def getHorizontalSeperator(self):
    horizontalLine = QtGui.QFrame()
    horizontalLine.setFrameStyle(QtGui.QFrame.HLine)
    horizontalLine.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    return horizontalLine
