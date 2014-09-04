"""
settings_tab_controller.py

Created by Scott Rice on 8-23-2014
"""

from ice.gui.tabs.settings_tab_widget import SettingsTabWidget
from PyQt4 import QtGui

class SettingsTabController(object):

  def __init__(self, config):
    self.widget = SettingsTabWidget()
    self.config = config

    self.widget.romsDirectoryDisplayWidget.setText(self.config.roms_directory())
    self.widget.backupDirectoryDisplayWidget.setText(self.config.backup_directory())
    if self.config.steam_userdata_location():
      self.widget.userdataWidget.setText(self.config.steam_userdata_location())

    self.widget.romButton.clicked.connect(self.romDirDialog)
    self.widget.backupButton.clicked.connect(self.backupDirDialog)

  def romDirDialog(self):
    dir = QtGui.QFileDialog.getExistingDirectory(self.widget, "Pick Roms Directory", self.config.roms_directory())
    self.config.set_roms_directory(str(dir))
    self.widget.romsDirectoryDisplayWidget.setText(self.config.roms_directory())

  def backupDirDialog(self):
    dir = QtGui.QFileDialog.getExistingDirectory(self.widget, "Pick Backup Directory", self.config.backup_directory())
    self.config.set_backup_directory(str(dir))
    self.widget.backupDirectoryDisplayWidget.setText(self.config.backup_directory())
