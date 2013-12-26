![Example of Ice](ice-example.png "Example")

##Ice

###Description

The purpose of this project is to leverage Steam's Big Picture mode to turn it into an emulator frontend (similar to Hyperspin). It accomplishes this by creating folders in specified locations on the user's hard drive, then adding any ROMs that are placed in these folders to Steam as non-Steam games. Emulators are installed and configured by the user before Ice is run.

###License

All of my code is licensed under MIT.

###Getting Started

Ice's official documentation is available at [Getting Started.](http://scottrice.github.io/Ice/getting-started/) 

###Running the Source

To run the source, besides the setup instructions, you will also need to have Python installed. Python 2.7 is required.

If you have Python installed, simply run `python ice.py` from the repository's root directory. On Mac/Linux, you should also be able to use the command `./ice.py` provided the file has the execute permission.

###Goal Updates

Originally, I wanted to make an application that would constantly 'watch' the ROMs folder and modify the shortcuts.vdf file as changes were made to the folder. I have since found out that Steam doesn't take kindly to having it's shortcuts.vdf file updated while it is running, and will overwrite any changes that are made to the file on close.

With this in mind, you now need to run Ice every time a change is made for it to update your shortcuts.vdf. This is not an ideal solution, and in the future I will see what I can do to make this experience better.

##Steam Grid Images

###Sources

The user can specify which website they want to use to source their Steam Grid Images. I put this is in so people have options, but my code isn't completely flexible. If someone wants to make their site a valid Grid Image Source, the request path needs to...

- Accept 2 arguments:
  - Name - The name of the ROM
  - Console - The shortname of the console this ROM is on. See below
- Respond with a 204 No Content if the game was not found
- Respond with the empty string if there is no picture for the game
- Respond with a URL, which is the URL of the picture to download (needs to be a full URL, not a path).
  
##Emulators

###Console Shortnames

Shortnames are used in many places. They are used as the folder names where the user puts ROMs, and are used in the URL of the Grid Image Source request. The full list of shortnames is below.

####Supported Consoles

* NES - Nintendo Entertainment System
* SNES - Super Nintendo
* N64 - Nintendo 64
* Gamecube - Nintendo Gamecube
* PS1 - Sony Playstation
* PS2 - Sony Playstation 2
* Genesis - Sega Genesis
* Gameboy - Nintendo Gameboy
* GBA - Nintendo Gameboy Advance

####Unsupported Consoles (which may be supported later)

* Wii - Nintendo Wii
* Dreamcast - Sega Dreamcast
* DS - Nintendo DS