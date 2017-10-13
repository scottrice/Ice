![Example of Ice](ice-example.png "Example")

## Ice

### Description

The purpose of this project is to leverage Steam's Big Picture mode to turn it into an emulator frontend (similar to Hyperspin). It accomplishes this by creating folders in specified locations on the user's hard drive, then adding any ROMs that are placed in these folders to Steam as non-Steam games. Emulators are installed and configured by the user before Ice is run.

### License

All of my code is licensed under MIT.

### Getting Started

Ice's official documentation is available at [Getting Started.](http://scottrice.github.io/Ice/getting-started/) 

### Running the Source

You will need Python 2.7 to run Ice. Python 3.0 and up will not work.

You will also need pip installed. The easiest way to get that is to run `easy_install pip`.

Next, you will need to download all of Ice's dependencies. To do so, run `python setup.py install`

Once all of that is finished, simply run `python -m ice` from the repository's root directory.

### Ice GUI

A GUI for Ice is currently being developed, but is very far from being production ready. As of writing, it is basically non-functional. Do not attempt to use the GUI, doing so will only bring you pain and heartache.
