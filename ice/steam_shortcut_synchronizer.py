
from pysteam import shortcuts

import roms

from consoles import console_roms_directory
from logs import logger

class SteamShortcutSynchronizer(object):

  def __init__(self, config, managed_rom_archive):
    self.config = config
    self.managed_rom_archive = managed_rom_archive

  def _guess_whether_shortcut_is_managed_by_ice(self, shortcut, consoles):
    # Helper function which guesses whether the shortcut was added during a
    # previous run of Ice with its console set as `console`. We do this the
    # same way we did before we had the flag tag, we check the console's
    # ROMs directory and see if it shows up in the executable for the shortcut
    def shortcut_is_managed_by_console(console):
      return console_roms_directory(self.config, console) in shortcut.exe

    return any(map(shortcut_is_managed_by_console, consoles))

  def shortcut_is_managed_by_ice(self, managed_ids, shortcut, consoles):
    # LEGACY: At one point I added ICE_FLAG_TAG to every shortcut Ice made.
    # That was a terrible idea, the managed_ids is a much better system. I
    # keep this check around for legacy reasons though.
    if roms.ICE_FLAG_TAG in shortcut.tags:
      return True
    # LEGACY: For most of Ice's life it guessed whether it managed a shortcut
    # or not. This was REALLY bad, as it was very dependent on configuration
    # and caused really strange bugs where moving directories would cause ROMs
    # to get duplicated and all sorts of bad stuff.
    #
    # Luckily, we have a history now and don't have to deal with that crap.
    # Yay! Except that this screws over anyone who used Ice //before// it had
    # a history, as we have no record of what they added before. Shit.
    #
    # To fix this, we provide a migration path for these people. If we have NO
    # history (not an empty history, NO history) then we fall back to our old
    # way of checking whether we manage the shortcut. The next time Ice is run
    # we will have a history to work with and can avoid using this hacky garbage.
    if managed_ids is None:
      return self._guess_whether_shortcut_is_managed_by_ice(shortcut, consoles)
    # We only 'manage' it if we added the shortcut in the last run
    return shortcuts.shortcut_app_id(shortcut) in managed_ids

  def unmanaged_shortcuts(self, managed_ids, shortcuts, consoles):
    return filter(
      lambda shortcut: not self.shortcut_is_managed_by_ice(managed_ids, shortcut, consoles),
      shortcuts,
    )

  def removed_shortcuts(self, current_shortcuts, new_shortcuts):
    # To get the list of only removed shortcuts we take all of the current
    # shortcuts and filter out any that exist in the new shortcuts
    return filter(lambda shortcut: shortcut not in new_shortcuts, current_shortcuts)

  def added_shortcuts(self, current_shortcuts, new_shortcuts):
    # To get the list of only added shortcuts we take all of the new shortcuts
    # and filter out any that existed in the current shortcuts
    return filter(lambda shortcut: shortcut not in current_shortcuts, new_shortcuts)

  def sync_roms_for_user(self, user, users_roms, consoles, dry_run=False):
    """
    This function takes care of syncing ROMs. After this function exits,
    Steam will contain only non-Ice shortcuts and the ROMs represented
    by `roms`.
    """
    # 'Unmanaged' is just the term I am using for shortcuts that the user has
    # added that Ice shouldn't delete. For example, something like a shortcut
    # to Plex would be 'Unmanaged'
    previous_managed_ids = self.managed_rom_archive.previous_managed_ids(user)
    logger.debug("Previous managed ids: %s" % previous_managed_ids)
    current_shortcuts = shortcuts.get_shortcuts(user)
    unmanaged_shortcuts = self.unmanaged_shortcuts(previous_managed_ids, current_shortcuts, consoles)
    logger.debug("Unmanaged shortcuts: %s" % unmanaged_shortcuts)
    current_ice_shortcuts = filter(lambda shortcut: shortcut not in unmanaged_shortcuts, current_shortcuts)
    logger.debug("Current Ice shortcuts: %s" % current_ice_shortcuts)
    # Generate a list of shortcuts out of our list of ROMs
    rom_shortcuts = map(roms.rom_to_shortcut, users_roms)
    # Calculate which ROMs were added and which were removed so we can inform
    # the user
    removed = self.removed_shortcuts(current_ice_shortcuts, rom_shortcuts)
    map(lambda shortcut: logger.info("Removing ROM: `%s`" % shortcut.name), removed)
    added = self.added_shortcuts(current_ice_shortcuts, rom_shortcuts)
    map(lambda shortcut: logger.info("Adding ROM: `%s`" % shortcut.name), added)

    # Set the updated shortcuts
    updated_shortcuts = unmanaged_shortcuts + rom_shortcuts
    logger.debug("Sync Result: %s" % updated_shortcuts)

    if dry_run:
      logger.debug("Not saving or updating history due to dry run")
      return

    logger.debug("Saving shortcuts")
    shortcuts.set_shortcuts(user, updated_shortcuts)

    # Update the archive
    new_managed_ids = map(shortcuts.shortcut_app_id, rom_shortcuts)
    logger.debug("Updating archive to ids: %s" % new_managed_ids)
    self.managed_rom_archive.set_managed_ids(user, new_managed_ids)
