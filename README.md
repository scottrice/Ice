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
use Steam's Big Picture mode to act as a ROM selector, so they can go and play
their favorite game on X console extremely easily, similar to how buddwm does
it in his NES/SNES PC build projects. You can find the videos I am talking
about here:

http://www.youtube.com/watch?feature=player_detailpage&v=cBtYiQ1mnvA#t=462s

Clearly this is just the software end, but hopefully this gives an idea of the
kind of user experience I am hoping for (pick a game from a list, immediately
get to play it, etc)

##TODO

- Watch specified folder for updates
  **Until I can identify how Steam deals with shortcuts being editing while it
  is open, I am going to make ice a "run to update" script
- Figure out any issues with referencing files that I include in my package.
  This will require additional time with setup.py, as it is still kind of
  magical to me.
- Add emulators to the package (possible issue with distribution?), or maybe
  even let the user use their own emulators.
- Create scripts that will open the ROM in a given emulator when run (this will
  be the shortcut "Exe" for Steam)
- Figure out possible issues with modifying shortcuts.vdf while Steam is
  currently running. Will we need a restart? This could very much alter our
  current 'ideal' user experience
  
##Goal Updates

Until I can identify issues with Steam and modifying shortcuts.vdf, I will code
under the assumption that Ice is run every time the user wants to 'update'
their list of shortcuts, as in we don't have to run constantly and watch the
folders, but instead we just run one update and exit. This will also help in
that since there is no persistant state, if Steam undoes all our changes
because it overwrote shortcuts.vdf on close, the user can just run Ice again
and all our changes will be redone.