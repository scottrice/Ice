Note that Mupen64Plus requires an Intel mac and will not run on PPC macs.
It is known to run on OS X 10.6; and most likely also runs on 10.5.

This application can NOT be opened in the Finder by double-clicking, because no graphical user interface is ready for mupen 2.0
yet. To use, launch the terminal, then cd into the directory that contains mupen64plus.app and use a command like :

    $ ./run_glide.sh example.v64        # for the Glide video plugin
    $ ./run_arach.sh example.v64        # for the Arachnoid video plugin
    $ ./run_rice.sh  example.v64        # for the Rice video plugin

Note that at this point, the only way to configure Mupen64Plus is to edit the config files in ~/.config/mupen64plus

If you cannot follow the instructions above then this package is not meant for you =)
