"""
emulators_tab_controller.py

Created by Scott Rice on 8-23-2014
"""

from ice.gui.tabs.emulators_tab_widget import EmulatorsTabWidget

class EmulatorsTabController(object):

  def __init__(self):
    self.widget = EmulatorsTabWidget()