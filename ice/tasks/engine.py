# encoding: utf-8

from ice.steam import steam as steam_module

from ice.logs import logger


class TaskEngine(object):

  def __init__(self, steam):
    self.steam = steam

    logger.debug("Initializing Ice")
    # We want to ignore the anonymous context, cause theres no reason to sync
    # ROMs for it since you cant log in as said user.
    self.users = [item for item in steam_module.local_user_contexts(self.steam) if item.user_id != 'anonymous']

  def run(self, tasks, app_settings, dry_run=False):
    if self.steam is None:
      logger.error("Cannot run Ice because Steam doesn't appear to be installed")
      return

    logger.info("=========== Starting Ice ===========")

    for task in tasks:
      task(app_settings, self.users, dry_run=dry_run)
