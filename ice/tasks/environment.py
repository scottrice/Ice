# encoding: utf-8

from pysteam import paths as steam_paths

from ice import consoles
from ice.environment_checker import EnvironmentChecker
from ice.error import HumanReadableError
from ice.error.env_checker_error import EnvCheckerError
from ice.logs import logger
from ice import paths

ERROR_MESSAGE_FORMAT = """\
Ice cannot run because of issues with your system.

* %s

Please resolve these issues and try running Ice again.\
"""

STEAM_CHECK_SKIPPED_WARNING = """\
Not checking whether Steam is running. Any changes made may be overwritten \
when Steam exits.\
"""

class PrepareEnvironmentTask(object):
  def __init__(self, filesystem, skip_steam_check):
    self.filesystem = filesystem
    self.skip_steam_check = skip_steam_check

  def __call__(self, app_settings, users, dry_run):
    try:
      self.validate_environment(app_settings, users)
    except EnvCheckerError as e:
      updated_message = ERROR_MESSAGE_FORMAT % e.message
      raise HumanReadableError(updated_message)

  def validate_environment(self, app_settings, users):
    """
    Validate that the current environment meets all of Ice's requirements.
    """
    with EnvironmentChecker(self.filesystem) as env_checker:
      if not self.skip_steam_check:
        # If Steam is running then any changes we make will be overwritten
        env_checker.require_program_not_running("Steam")
      else:
        logger.warning(STEAM_CHECK_SKIPPED_WARNING)
      # This is used to store history information and such
      env_checker.require_directory_exists(paths.application_data_directory())

      for console in app_settings.consoles:
        # Consoles assume they have a ROMs directory
        env_checker.require_directory_exists(consoles.console_roms_directory(app_settings.config, console))

      for user in users:
        # I'm not sure if there are situations where this won't exist, but I
        # assume that it does everywhere and better safe than sorry
        env_checker.require_directory_exists(user.steam.userdata_directory)
        # If the user hasn't added any grid images on their own then this
        # directory wont exist, so we require it explicitly here
        env_checker.require_directory_exists(steam_paths.custom_images_directory(user))
        # And it needs to be writable if we are going to save images there
        env_checker.require_writable_path(steam_paths.custom_images_directory(user))
