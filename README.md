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