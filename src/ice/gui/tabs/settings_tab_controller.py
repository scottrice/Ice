"""
settings_tab_controller.py

Created by Scott Rice on 8-23-2014
"""

from ice.gui.tabs.settings_tab_widget import SettingsTabWidget

class SettingsTabController(object):

  def __init__(self, config):
    self.widget = SettingsTabWidget()
    self.config = config

    self.widget.romsDirectoryWidget.setText(config.roms_directory())
    self.widget.backupDirectoryWidget.setText(config.backup_directory())
    if config.steam_userdata_location():
      self.widget.userdataWidget.setText(config.steam_userdata_location())