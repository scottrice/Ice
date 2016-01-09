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
* unknowno
  * dunno if needed: libxrandr2:i386(was in old setup script)

# Man page notes

## Investigate / augment Parsers
```
parser.add_argument('-c', '--config', type=str, default=None)
    parser.add_argument('-C', '--consoles', type=str, default=None)
    parser.add_argument('-e', '--emulators', type=str, default=None)
    # Debugging options
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-d', '--dry-run', action='store_true')
```
