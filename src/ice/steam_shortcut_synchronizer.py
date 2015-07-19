
from rom import ICE_FLAG_TAG

class SteamShortcutSynchronizer(object):

  def __init__(self, managed_rom_archive, logger):
    self.managed_rom_archive = managed_rom_archive
    self.logger = logger

  def shortcut_is_managed_by_ice(self, managed_ids, shortcut):
    # LEGACY: At one point I added ICE_FLAG_TAG to every shortcut Ice made.
    # That was a terrible idea, the managed_ids is a much better system. I
    # keep this check around for legacy reasons though.
    if ICE_FLAG_TAG in shortcut.tags:
      return True
    if managed_ids is None:
      # No history, nothing we can do other than assume they haven't run Ice
      # before
      return False
    # We only 'manage' it if we added the shortcut in the last run
    return shortcut.appid() in managed_ids

  def unmanaged_shortcuts(self, managed_ids, shortcuts):
    return filter(lambda shortcut: not self.shortcut_is_managed_by_ice(managed_ids, shortcut), shortcuts)

  def removed_shortcuts(self, current_shortcuts, new_shortcuts):
    # To get the list of only removed shortcuts we take all of the current
    # shortcuts and filter out any that exist in the new shortcuts
    return filter(lambda shortcut: shortcut not in new_shortcuts, current_shortcuts)

  def added_shortcuts(self, current_shortcuts, new_shortcuts):
    # To get the list of only added shortcuts we take all of the new shortcuts
    # and filter out any that existed in the current shortcuts
    return filter(lambda shortcut: shortcut not in current_shortcuts, new_shortcuts)

  def sync_roms_for_user(self, user, roms):
    """
    This function takes care of syncing ROMs. After this function exits,
    Steam will contain only non-Ice shortcuts and the ROMs represented
    by `roms`.
    """
    # 'Unmanaged' is just the term I am using for shortcuts that the user has
    # added that Ice shouldn't delete. For example, something like a shortcut
    # to Plex would be 'Unmanaged'
    previous_managed_ids = self.managed_rom_archive.previous_managed_ids(user)
    unmanaged_shortcuts = self.unmanaged_shortcuts(previous_managed_ids, user.shortcuts)
    current_ice_shortcuts = filter(lambda shortcut: shortcut not in unmanaged_shortcuts, user.shortcuts)
    # Generate a list of shortcuts out of our list of ROMs
    rom_shortcuts = map(lambda rom: rom.to_shortcut(), roms)
    # Calculate which ROMs were added and which were removed so we can inform
    # the user
    removed = self.removed_shortcuts(current_ice_shortcuts, rom_shortcuts)
    map(lambda shortcut: self.logger.info("Removing ROM: `%s`" % shortcut.name), removed)
    added = self.added_shortcuts(current_ice_shortcuts, rom_shortcuts)
    map(lambda shortcut: self.logger.info("Adding ROM: `%s`" % shortcut.name), added)

    # Set the updated shortcuts
    user.shortcuts = unmanaged_shortcuts + rom_shortcuts
    user.save_shortcuts()

    # Update the archive
    new_managed_ids = map(lambda shortcut: shortcut.appid(), rom_shortcuts)
    self.managed_rom_archive.set_managed_ids(user, new_managed_ids)
