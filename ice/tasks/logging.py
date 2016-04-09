#!/usr/bin/env python
# encoding: utf-8

from ice.logs import logger

# TODO(#368); This shouldn't be necessary as part of the app. We shouldn't be
# relying on log messages as our UI
class LogAppStateTask(object):

  def __call__(self, app_settings, users, dry_run):
    for emulator in app_settings.emulators:
      logger.info("Detected Emulator: %s" % emulator.name)

    for console in app_settings.consoles:
      logger.info("Detected Console: %s => %s" % (console.fullname, console.emulator.name))

    if len(users) is 0:
      logger.info("No users were found in Steam's userdata, so Ice has no shortcuts to set. Has anyone logged in on this computer before?")
      return

    user_ids = map(lambda u: u.user_id, users)
    logger.info("===== Running for users: %s =====" % ", ".join(user_ids))
