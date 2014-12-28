"""
sync_tab_controller.py

Created by Scott Rice on 8-23-2014
"""

from ice.gui.tabs.sync_tab_widget import SyncTabWidget


class SyncTabController(object):

  # TODO: Runner shouldn't be passed to SyncTabWidget here, it should pass in
  # only the data needed when the tab widget needs it. The tab widget (and steam
  # preview widget) shouldnt be holding onto that information as state.

  def __init__(self, engine, statusBar):
    self.windowStatusBar = statusBar
    self.widget = SyncTabWidget()
    self.engine = engine
    self.users = engine.users

    self.widget.populateUsersDropdownWithUsers(self.users)
    self.user = self.users[self.widget.selectedUserIndex()]
    self.widget.setPreviewForUser(self.user)

    self.widget.setUserChangedCallback(self.onUserChanged)
    self.widget.setOnSyncCallback(self.sync)
    self.widget.setROMs(engine.config.valid_roms())

    self.windowStatusBar.showMessage("Ready")

  def onUserChanged(self, index):
    self.user = self.users[index]

  def sync(self):
    self.windowStatusBar.showMessage("Running Ice for %i" % self.user.id32)
    self.engine.run_for_user(self.user)
    self.windowStatusBar.showMessage("Done", 5000)
