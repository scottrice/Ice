
from ice.rom import ICE_FLAG_TAG

class SteamShortcutSynchronizer(object):

  def __init__(self, managed_rom_archive, logger):
    self.managed_rom_archive = managed_rom_archive
    self.logger = logger

  def shortcut_is_managed_by_ice(self, managed_ids, shortcut):
    return shortcut.appid() in managed_ids or ICE_FLAG_TAG in shortcut.tags

  def unmanaged_shortcuts(self, managed_ids, shortcuts):
    return list(filter(lambda shortcut: not self.shortcut_is_managed_by_ice(managed_ids, shortcut), shortcuts))

  def removed_shortcuts(self, current_shortcuts, new_shortcuts):
    # To get the list of only removed shortcuts we take all of the current
    # shortcuts and filter out any that exist in the new shortcuts
    return [shortcut for shortcut in current_shortcuts if shortcut not in new_shortcuts]

  def added_shortcuts(self, current_shortcuts, new_shortcuts):
    # To get the list of only added shortcuts we take all of the new shortcuts
    # and filter out any that existed in the current shortcuts
    return [shortcut for shortcut in new_shortcuts if shortcut not in current_shortcuts]

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
    current_ice_shortcuts = list(filter(lambda shortcut: shortcut not in unmanaged_shortcuts, user.shortcuts))
    # Generate a list of shortcuts out of our list of ROMs
    rom_shortcuts = list(map(lambda rom: rom.to_shortcut(), roms))
    # Calculate which ROMs were added and which were removed so we can inform
    # the user
    removed = self.removed_shortcuts(current_ice_shortcuts, rom_shortcuts)
    for shortcut in removed:
        self.logger.info("Removing ROM: `%s`" % shortcut.name)
    added = self.added_shortcuts(current_ice_shortcuts, rom_shortcuts)
    for shortcut in added:
        self.logger.info("Adding ROM: `%s`" % shortcut.name)

    # Set the updated shortcuts
    user.shortcuts = unmanaged_shortcuts + rom_shortcuts
    user.save_shortcuts()

    # Update the archive
    new_managed_ids = list(map(lambda shortcut: shortcut.appid(), rom_shortcuts))
    self.managed_rom_archive.set_managed_ids(user, new_managed_ids)
