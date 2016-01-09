#!/bin/bash

# Cleans project files for manual build attempts and builds

# Debian packages required
sudo apt-get install -y --force-yes libxrandr2:i386 python-pip python-psutil

# uninstall python applications
sudo pip uninstall pysteam
sudo pip uninstall pysteam-steamos 
sudo pip uninstall appdirs

# Remove project files
sudo rm -rf /tmp/pip_build_root
sudo rm -rf build
sudo rm -rf Ice.egg-info
sudo rm -rf dist

# Attemp new project build
sudo pip install -r requirements.txt
sudo python setup.py install

# Run info
echo -e "\nAttempt to run 'python -m ice'\n"
