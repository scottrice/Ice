##Description

The purpose of this project is to leverage Steam's Big Picture mode to turn it
into an emulator frontend (similar to Hyperspin). It accomplishes this by
creating folders in specified locations on the users hard drive, and when a ROM
is placed in one of those folders, my application will automatically add it to
Steam as a non-steam game. Emulators to run each game should come 
pre-configured to support Xbox 360 controllers intelligently while still 
allowing all Steam features to be accessible (community etc)

##TODO

- Watch specified folder for updates
  **Until I can identify how Steam deals with shortcuts being editing while it
  is open, I am going to make ice a "run to update" script
- Figure out possible issues with modifying shortcuts.vdf while Steam is
  currently running. Will we need a restart? This could very much alter our
  current 'ideal' user experience
- Figure out issues with changing discs in the PS1 emulator
- Add more controller shortcuts for various things. One thing I would like is a
  shortcut to pause the game (maybe SELECT+A?). I'm sure there are other useful
  things that could be done, although you would need to teach it to the user
  somehow.
- Include artwork with the games. This will require a significant amount of
  code, and I'm pretty sure will require a website to manage people's
  favorites. I will most likely go the route I did with the Steam Shortcut
  Manager and split it off into another project which I will integrate later.
  
##Goal Updates

Until I can identify issues with Steam and modifying shortcuts.vdf, I will code
under the assumption that Ice is run every time the user wants to 'update'
their list of shortcuts, as in we don't have to run constantly and watch the
folders, but instead we just run one update and exit. This will also help in
that since there is no persistant state, if Steam undoes all our changes
because it overwrote shortcuts.vdf on close, the user can just run Ice again
and all our changes will be redone.

##License

All of my code is licensed under MIT.

##Emulator License Issues

Most of the emulators use permissive licenses. The most common are MIT and GPL.
A few include clauses that they are only to be used for personal use, so if you
want to use my code for commercial use you need to get different emulators.

To switch out an emulator, check the emulator_manager.

##BIOS Issues

With the inclusion of PS1 emulators and PS2 emulators, which require a legal
BIOS to run, I would like to point out that the only way of legally using the
emulators is to dump your Playstations BIOS yourself. If you are curious, there
are plenty of guides online describing how to do it.