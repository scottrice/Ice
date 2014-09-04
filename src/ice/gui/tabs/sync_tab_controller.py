"""
sync_tab_controller.py

Created by Scott Rice on 8-23-2014
"""

from ice.gui.tabs.sync_tab_widget import SyncTabWidget

class SyncTabController(object):

  # TODO: Runner shouldn't be passed to SyncTabWidget here, it should pass in
  # only the data needed when the tab widget needs it. The tab widget (and steam
  # preview widget) shouldnt be holding onto that information as state.
  def __init__(self, runner):
    self.widget = SyncTabWidget()
    self.runner = runner
    self.users  = runner.users

    self.widget.populateUsersDropdownWithUsers(self.users)
    self.user = self.users[self.widget.selectedUserIndex()]
    self.widget.setPreviewForUser(self.user)

    self.widget.setUserChangedCallback(self.onUserChanged)
    self.widget.setOnSyncCallback(self.sync)
    self.widget.setROMs(runner.config.valid_roms())

  def onUserChanged(self, index):
    self.user = self.users[index]
    print self.user.id32

  def sync(self):
    self.runner.run_for_user(self.user)