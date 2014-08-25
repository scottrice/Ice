"""
consoles_tab_controller.py

Created by Scott Rice on 8-23-2014
"""

from ice.gui.tabs.consoles_tab_widget import ConsolesTabWidget

class ConsolesTabController(object):

  def __init__(self, config):
    self.widget = ConsolesTabWidget()
    self.config = config