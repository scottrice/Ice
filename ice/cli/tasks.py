# encoding: utf-8

from ice.parsing.rom_parser import ROMParser
from ice.rom_finder import ROMFinder
from ice.tasks import LaunchSteamTask, \
                      LogAppStateTask, \
                      PrepareEnvironmentTask, \
                      SyncShortcutsTask, \
                      UpdateGridImagesTask \

class TaskCoordinator(object):

  def __init__(self, filesystem):
    self.filesystem = filesystem

    self.rom_finder = ROMFinder(self.filesystem, ROMParser())

  def tasks_for_options(self, launch_steam = False, skip_steam_check = False):
    tasks = [
      PrepareEnvironmentTask(self.filesystem, skip_steam_check),
      LogAppStateTask(),
      SyncShortcutsTask(self.rom_finder),
    ]

    if launch_steam:
      tasks = tasks + [ LaunchSteamTask() ]

    tasks = tasks + [ UpdateGridImagesTask(self.rom_finder) ]
    return tasks
