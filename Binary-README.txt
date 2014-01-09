================================================================================
Setup:

Open emulators.txt and make an entry for every emulator you wish to use.
If you are not sure how to add an emulator to the file, check out

http://scottrice.github.io/Ice/emulators

for example configurations for a lot of popular emulators. The entries on the
site should be available to copy-paste, but you will need to update the location
to the actual file location on your machine.

Once you have an entry in emulators.txt for every emulator you want to use, go
to consoles.txt. Make an entry for every console you would like to use (though
the more popular ones should already have entries created). Next, under
'emulator', put the name of the emulator you created in emulators.txt. For
example, if you have an emulator set up like this:

[Awesome Emulator]
location=C:\Path\to\awesomeemu.exe

And you would like to use it for your Sweet Console, consoles.txt would look
like this:

[Sweet Console]
emulator=Awesome Emulator

Once that is done, run Ice. Ice should output messages letting you know that
it detected your emulators/consoles.

================================================================================
Using Ice:

1) Run Ice once. Confirm that it found your emulators/consoles. This also
creates a directory at C:\Users\*username*\ROMs (or ~/ROMs on Mac/Linux).
2) Open the directory mentioned above (the 'ROMs directory'). There should be
a subdirectory for every console that has an emulator attached
3) Drop your ROMs into the subdirectory for the console. For example, if you
wanted to add 'Super Mario World' for the SNES, you would put the ROM inside of
C:\Users\*username*\ROMs\SNES.
4) Run Ice again. You should get a message that Ice has added the game to Steam.
5) Play!

================================================================================
Help!

If you are having trouble with setup, check out

http://scottrice.github.io/Ice/getting-started

If you have question, go to

http://scottrice.github.io/Ice/faq

If neither of the above links are helpful, try posting an issue to

http://github.com/scottrice/Ice/issues
