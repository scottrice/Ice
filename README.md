##Description
The purpose of this application is to turn Steam's Big Picture mode into a
retro console gaming paradise. This application accomplishes this in two ways,
the first is by coming bundled with a set of emulators pre-set up with an Xbox
controller in mind (Xbox only because of how well supported it is in Windows).
The second is to 'watch' a predetermined set of directories, and when a ROM is
added to any of those directories, having it added to Steam.

While this is not the only experience I hope to enable via this application,
the driving goal behind this application is to allow someone to download all
of the ROMs for a certain system, throw them in a folder, and then be able to
use Steam's Big Picture mode to act as a ROM chooser, so they can go and play
their favorite game on X console extremely easily, similar to how buddwm does
it in his NES/SNES PC build projects. You can find the videos I am talking
about here: 

##TODO

- Find list of users for a system, possibly let users choose the 'current' user
- Watch specified folder for updates
- Create folders to watch if they don't exist
- Create a list of ROMs based on the files in those folders (a ROM should have
  a name, a path, and a console)
- Get the list of shortcuts the user currently has in their shortcuts.vdf file
- Sync the ROMs that we found in the folders with the shortcuts that are 
  already in shortcuts.vdf. Possibly need to add some sort of marker that lets
  me know a shortcut was added by Ice