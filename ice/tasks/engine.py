# encoding: utf-8

import os

from pysteam import paths as steam_paths
from pysteam import shortcuts
from pysteam import steam as steam_module

from ice import backups
from ice import configuration
from ice import consoles
from ice import emulators
from ice import paths
from ice import settings
from ice.logs import logger
from ice.persistence.config_file_backing_store import ConfigFileBackingStore

class TaskEngine(object):

  def __init__(self, steam, filesystem, app_settings):
    self.steam = steam
    self.filesystem = filesystem

    # We want to ignore the anonymous context, cause theres no reason to sync
    # ROMs for it since you cant log in as said user.
    is_user_context = lambda context: context.user_id != 'anonymous'
    self.users = filter(is_user_context, steam_module.local_user_contexts(self.steam))

    logger.debug("Initializing Ice")

    self.app_settings = app_settings

  def run(self, tasks, dry_run=False):
    if self.steam is None:
      logger.error("Cannot run Ice because Steam doesn't appear to be installed")
      return

    logger.info("=========== Starting Ice ===========")

    for task in tasks:
      task(self.app_settings, self.users, dry_run=dry_run)
