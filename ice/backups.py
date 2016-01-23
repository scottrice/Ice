# encoding: utf-8

import datetime
import os

from pysteam import shortcuts

import paths

from logs import logger

def default_backups_directory():
  return os.path.join(paths.application_data_directory(), 'Backups')

def backup_filename(user, timestamp_format):
  timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
  return "shortcuts." + timestamp + ".vdf"

def shortcuts_backup_path(directory, user, timestamp_format="%Y%m%d%H%M%S"):
  """
  Returns the path for a shortcuts.vdf backup file.

  This path is in the designated backup directory, and includes a timestamp
  before the extension to allow many backups to exist at once.
  """
  assert(directory is not None)
  return os.path.join(
      directory,
      str(user.user_id),
      backup_filename(user, timestamp_format)
  )

def backup_directory(config):
  backup_dir = config.backup_directory
  if backup_dir is None:
    return None

  if backup_dir == "":
    backup_dir = default_backups_directory()
    logger.debug("Specified empty string as backup directory. Defaulting to %s" % backup_dir)
  return backup_dir

def create_backup_of_shortcuts(config, user, dry_run=False):
  def _create_directory_if_needed(directory):
    if os.path.exists(directory):
      return

    logger.debug("Creating directory: %s" % directory)
    os.makedirs(directory)

  backup_dir = backup_directory(config)
  if backup_dir is None:
    logger.info("No backups directory specified, so not backing up shortcuts.vdf before overwriting. See config.txt for more info")
    return

  _create_directory_if_needed(backup_dir)

  if not os.path.isdir(backup_dir):
    logger.warning("Backup directory path is something other than a directory. Skipping backups")
    return

  backup_path = shortcuts_backup_path(backup_dir, user)

  # Make sure the user-specific backups dir exists
  _create_directory_if_needed(os.path.dirname(backup_path))

  shortcuts.write_shortcuts(backup_path, shortcuts.get_shortcuts(user))
