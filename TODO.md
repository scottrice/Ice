# Main items

* config files either gone and all hardcoded or move config files
* launch script
* do things in home directories! Like creating roms directories and searching for roms
* init script to update, but only if changes have been made
*  emulators as dependencies for package and fully configured for launch

# Actual requirements checks

* Debian
  * zsnes mupen64plus python-pip(if used for installing) python-psutil(also available with pip)
* python
  * pysteam appdirs
* unknown
  * dunno if needed: libxrandr2:i386(was in old setup script)

# Man page notes

## Creating / maintaining
[creating (nixcraft)](http://www.cyberciti.biz/faq/linux-unix-creating-a-manpage/)

Example to use:
```
.\" Manpage for ice.
.\" Contact ser@mail.net.in to correct errors or typos.
.TH man 8 "08 Jan 2016" "1.0" "ice man page"
.SH NAME
ice \- Utility to add ROMs to Steam BPM and make launching them much easier.
.SH SYNOPSIS
ice-launcher [DIR]
.SH DESCRIPTION
This is an effort to make Ice, a tool which can add ROMs to your Steam library, work in SteamOS. All credit for the original application goes to the user scottrice.
.SH OPTIONS
TODO
.SH SEE ALSO
TODO
man(5)
.SH BUGS
No known bugs.
.SH AUTHOR
SteamOS version: ProfessorKaos64 (mdeguzis@gmail.com), Sharkwouter (https://github.com/sharkwouter)
Original source code: Scott Rice (https://github.com/scottrice/Ice)
```

## Investigate / augment Parsers
```
parser.add_argument('-c', '--config', type=str, default=None)
    parser.add_argument('-C', '--consoles', type=str, default=None)
    parser.add_argument('-e', '--emulators', type=str, default=None)
    # Debugging options
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-d', '--dry-run', action='store_true')
```
