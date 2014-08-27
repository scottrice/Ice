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
    # TODO: Will this break on machines where no user has logged into steam yet?
    self.user   = runner.users[0]
    self.widget = SyncTabWidget(self.user)
    self.runner = runner

    self.widget.setROMs(runner.config.valid_roms())
    for u in runner.users:
      self.widget.userDropdown.addItem(str(u.id32))

  def sync(self):
    self.runner.run()