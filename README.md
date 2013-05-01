![Example of Ice](ice-example.png "Example")

##Description

The purpose of this project is to leverage Steam's Big Picture mode to turn it
into an emulator frontend (similar to Hyperspin). It accomplishes this by
creating folders in specified locations on the users hard drive, and when a ROM
is placed in one of those folders, my application will automatically add it to
Steam as a non-steam game. Emulators to run each game should come 
pre-configured to support Xbox 360 controllers intelligently while still 
allowing all Steam features to be accessible (community etc)

##Grid Image Source
The user can specify which website they want to use to source their Steam Grid
Images. I put this is in so people have options, but my code isn't completely
flexible. If someone wants to make their site a valid Grid Image Source, the
request path needs to...

- Accept 2 arguments:
  - Name - The name of the ROM
  - Console - The shortname of the console this ROM is on. See below
- Respond with a 204 No Content if the game was not found
- Respond with the empty string if there is no picture for the game
- Respond with a URL, which is the URL of the picture to download (needs to be
  a full URL, not a path).
  
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

##Console Shortnames
Shortnames are used in many places. They are used as the folder names where the
user puts ROMs, and are used in the URL of the Grid Image Source request. The
full list of shortnames is below

###Supported Consoles

* NES - Nintendo Entertainment System
* SNES - Super Nintendo
* N64 - Nintendo 64
* Gamecube - Nintendo Gamecube
* PS1 - Sony Playstation
* PS2 - Sony Playstation 2
* Genesis - Sega Genesis
* Gameboy - Nintendo Gameboy
* GBA - Nintendo Gameboy Advance

###Unsupported Consoles (which may be supported later)

* Wii - Nintendo Wii
* Dreamcast - Sega Dreamcast
* DS - Nintendo DS
