#!/usr/bin/env python
# encoding: utf-8
"""
build.py

Created by Scott on 2013-10-03.
Copyright (c) 2013 Scott Rice. All rights reserved.

Code to generate an exe file out of Ice, along with any extra metadata needed.
"""

import os

import subprocess
import datetime
import zipfile
import shutil

ice_dir = os.path.dirname(os.path.realpath(__file__))
dist_dir = os.path.join(ice_dir,"dist")
zip_dir = os.path.join(dist_dir,"Ice")

def remove_previous_builds():
	"""Remove all of the artifacts from previous builds"""
	def remove_if_needed(path):
		if os.path.exists(path):
			shutil.rmtree(path)
	remove_if_needed(os.path.join(ice_dir,"build"))
	remove_if_needed(dist_dir)

def create_zip_directory():
	"""Creates a directory called 'Ice' inside dist that will be zipped"""
	os.makedirs(zip_dir)

def build_exe():
	command = "python %s/pyinstaller/pyinstaller.py --onefile --icon=icon.ico ice.py" % ice_dir
	subprocess.call(command)

def add_file(name, directory, new_name=None):
	"""Adds a file named 'name' in 'directory' to the zip directory"""
	if new_name is None:
		new_name = name
	src = os.path.join(directory, name)
	dst = os.path.join(zip_dir, new_name)
	shutil.copyfile(src, dst)

def add_extra_files():
	shutil.move(os.path.join(dist_dir,"ice.exe"),os.path.join(zip_dir,"Ice.exe"))
	add_file("config.txt",ice_dir)
	add_file("Binary-README.txt",ice_dir,"README.txt")
	add_file("ExitCombo.cfg",os.path.join(ice_dir,"config"),"ExitCombination.cfg")

def add_version_file():
	pfgit = os.path.join("C:/", "Program Files (x86)","Git","bin","git.exe")
	pfgit_exists = os.path.exists(pfgit)
	pfx86git = os.path.join("C:/", "Program Files (x86)","Git","bin","git.exe")
	pfx86git_exists = os.path.exists(pfx86git)
	if not pfgit_exists and not pfx86git_exists:
		# Whoever is building this doesn't have git installed, so I can't get
		# the revision. In that case, bail.
		return
	if pfgit_exists:
		git = pfgit
	else:
		git = pfx86git
	git_rev = subprocess.check_output("%s rev-parse --short HEAD" % git).strip()
	current_time = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
	version_path = os.path.join(zip_dir,"version.txt")
	version_file = open(version_path,"w+")
	version_file.write("Built at %s\n\nRevision %s" % (current_time, git_rev))

def zip_everything():
	# Taken from http://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory-in-python
	ice_zip = zipfile.ZipFile(os.path.join(dist_dir,'ice.zip'), 'w')
	for root, dirs, files in os.walk(zip_dir):
		for f in files:
			ice_zip.write(os.path.join(root, f),os.path.join("Ice",f))
	ice_zip.close()

def main():
	remove_previous_builds()
	create_zip_directory()
	build_exe()
	add_extra_files()
	add_version_file()
	zip_everything()

if __name__ == "__main__":
	main()