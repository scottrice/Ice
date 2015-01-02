#!/usr/bin/env python
"""
Installs a symlink from the `.git/hooks` directory to the `tools/git-hooks`
directory, thereby keeping all of our git hooks in version control
"""
import glob
import os
import platform
import shutil
import subprocess
import sys

from subprocess import call

WINDOWS_VERSION_NEEDS_TESTING_ERROR_MESSAGE = """
This script does not work on Windows. I would like to support it, but only
have spotty access to a Windows system. If you are interested in this, please
comment on Issue #245"""

GIT_HOOKS_ALREADY_EXIST_ERROR_MESSAGE = """
There are existing git hooks. This script will not remove them, so it is up to
you to decide whether you want to merge them or if you want to just forego
using Ice's default hooks (not recommended, as it will make merging your pull
requests much harder)

If you have hooks that you believe would be useful to Ice though, please put
them in the `git-hooks` directory and make a pull request.
"""

class WindowsSymlinkAdapter(object):
  def __init__(self):
    print WINDOWS_VERSION_NEEDS_TESTING_ERROR_MESSAGE
    sys.exit(1)
    # Real attempted implementation
    import win32file
    self.win32file = win32file

  def exists_at_path(self, path):
    pass

  def create(self, name, target):
    self.win32file.CreateSymbolicLink(fileSrc, fileTarget, 1)

class UnixSymlinkAdapter(object):

  def exists_at_path(self, path):
    return os.path.islink(path)

  def create(self, name, target):
    os.symlink(target, name)

def find_path_to_git_root():
  return subprocess.check_output(["git","rev-parse","--show-cdup"]).strip()

def remove_preexisting_hooks_dir(hooks_directory):
  """Checks the filesystem to see if the user has any custom hooks already set
  up before we blow away his hooks directory.

  Specifically, this function looks for two things in the hooks directory:

  * If the directory exists
  * If its empty
  * If it only contains the default sample git hooks

  In any of these cases this function considers it to be OK to remove the hooks
  directory and returns False. Otherwise, it assumes the user has made their
  own hooks and returns True"""
  if not os.path.exists(hooks_directory):
    return False
  hooks = os.listdir(hooks_directory)
  if len(hooks) == 0:
    print "Removing empty hooks directory"
    shutil.rmtree(hooks_directory)
    return False
  samples = glob.glob(os.path.join(hooks_directory, "*.sample"))
  if len(hooks) == len(samples):
    print "Removing sample hooks directory"
    shutil.rmtree(hooks_directory)
    return False
  return True


def create_hooks_symlink(adapter, target_hooks_path):
  """Creates a symlink at `.git/hooks` pointing to `path` (path being relative
  to the top of the git repository)"""
  root_relative_path = find_path_to_git_root()
  target_hooks_path = os.path.abspath(os.path.join(root_relative_path, target_hooks_path))
  install_path = os.path.abspath(os.path.join(root_relative_path, '.git', 'hooks'))

  if adapter.exists_at_path(install_path):
    # This script has already been run, we're done
    sys.exit(0)

  print "Installing symlink into %s" % install_path

  if remove_preexisting_hooks_dir(install_path):
    print GIT_HOOKS_ALREADY_EXIST_ERROR_MESSAGE
    sys.exit(1)

  adapter.create(install_path, target_hooks_path)

def main():
  adapter = WindowsSymlinkAdapter() if platform.system() == 'Windows' else UnixSymlinkAdapter()
  create_hooks_symlink(adapter, os.path.join('tools', 'git-hooks'))

if __name__ == '__main__':
  main()
