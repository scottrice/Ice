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
  
##Goal Updates

Until I can identify issues with Steam and modifying shortcuts.vdf, I will code
under the assumption that Ice is run every time the user wants to 'update'
their list of shortcuts, as in we don't have to run constantly and watch the
folders, but instead we just run one update and exit. This will also help in
that since there is no persistant state, if Steam undoes all our changes
because it overwrote shortcuts.vdf on close, the user can just run Ice again
and all our changes will be redone.

##License

All of my code is licensed under MIT. The emulators (some of which I include in
the git repo) are under a completely different license, which I try to make a
point of including. If someone wants to use my application for a use which is
not allowed by any license of any included emulators, it is up to said person
to make sure they remove said emulators and replace it with one whose terms
they dont violate

##Emulator License Issues

I am using this application for personal use, and assume that most people
interested in downloading my application will use it for personal use, so when
bundling emulators in my repo I assume that there is no commercial use 
involved (so things like the MIT license with a non-commercial clause is fine).
For the GPL, as far as I can tell from reading it, executing the GPLd code 
should not require me to GPL my own application as well. I am not a lawyer 
though, so any of the things I just said could be very wrong, but that is my 
understanding for now, and those are the assumptions I am going to work under 
until I can find someone who tells me otherwise