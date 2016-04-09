"""
command_line_runner.py

Created by Scott on 2014-08-14.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

import argparse

from pysteam.steam import get_steam, Steam

import tasks

from ice import decorators
from ice import debug
from ice import settings
from ice.logs import logger
from ice.filesystem import RealFilesystem
from ice.tasks import TaskEngine

def handle_exception(e, fatal):
  # Just log it
  if fatal:
    logger.exception("An exception occurred while running Ice")
  else:
    logger.error(e.message)

class CommandLineRunner(object):

  def __init__(self, steam=None, filesystem=None):
    self.steam = steam
    self.filesystem = RealFilesystem() if filesystem is None else filesystem

  def get_command_line_args(self, argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('pdebug', type=bool, nargs='?', help="Pastes debug logs to pastebin to include with bug reports.")
    parser.add_argument('--skip-steam-check', action='store_true', help="Skips checking whether Steam is running")
    parser.add_argument('--launch-steam', action='store_true', help="Launches Steam after the shortcuts have been synced and its safe to do so")
    # Config options
    parser.add_argument('-c', '--config', type=str, default=None)
    parser.add_argument('-C', '--consoles', type=str, default=None)
    parser.add_argument('-e', '--emulators', type=str, default=None)
    # Debugging options
    parser.add_argument('-d', '--dry-run', action='store_true')
    return parser.parse_args(argv)

  def should_use_user_override(self, override):
    if override is None:
      return False
    if override == "":
      return False
    if not self.filesystem.path_exists(override):
      logger.warning("config.txt specifies a Steam userdata directory that doesn't exist. Ignoring.")
      return False
    return False

  def get_steam(self, config):
    override = config.userdata_directory
    if self.should_use_user_override(override):
      return Steam(override)

    if self.steam is not None:
      return self.steam

    return get_steam()

  @decorators.catch_exceptions(handle_exception)
  def run(self, argv):
    opts = self.get_command_line_args(argv[1:])

    if opts.pdebug is True:
      debug.paste_debug_logs()
      return

    task_coordinator = tasks.TaskCoordinator(self.filesystem)

    app_settings = settings.load_app_settings(self.filesystem, file_overrides = {
        'config.txt': opts.config,
        'consoles.txt': opts.consoles,
        'emulators.txt': opts.emulators,
    })

    engine = TaskEngine(
      self.get_steam(app_settings.config),
    )

    tasks_to_run = task_coordinator.tasks_for_options(
      launch_steam = opts.launch_steam,
      skip_steam_check = opts.skip_steam_check,
    )

    engine.run(
      tasks = tasks_to_run,
      app_settings = app_settings,
      dry_run=opts.dry_run
    )
