#!/bin/bash

# Cleans project files for manual build attempts and builds

# uninstall python applications
sudo pip uninstall pysteam appdirs

# Remove project files
sudo rm -rf /tmp/pip_build_root
sudo rm -rf build
sudo rm -rf Ice.egg-info
sudo rm -rf dist

# Attemp new project build
sudo pip install --upgrade pysteam appdirs
sudo python setup.py install

# Run info
echo -e "\nAttempt to run 'python -m ice'\n"
