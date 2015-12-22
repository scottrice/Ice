# encoding: utf-8

import os
import random
import shutil
import tempfile

from pysteam import model
from pysteam import paths

class SteamFixture(object):
  def __init__(self):
    # This has the side effect of making the directory I need
    self.tempdir = tempfile.mkdtemp()

  def tearDown(self):
    # Check to make sure we haven't run this already
    if self.tempdir is None:
      return
    # Depending on the object graph this method may have been called before, so
    # check that the path exists before we try to remove it.
    assert(os.path.exists(self.tempdir))
    shutil.rmtree(self.tempdir)
    self.tempdir = None

  def get_steam(self):
    assert(self.tempdir is not None, "Should not have been cleaned up")
    return model.Steam(self.tempdir)

class UserFixture(object):
  def __init__(self, steam_fixture):
    self.steam_fixture = steam_fixture
    # No real special reasoning behind these numbers, just arbitrarys
    self.uid = str(random.randint(5, 2000))
    # Make all of the directories that Steam normally creates for a user
    self._create_default_directories()

  def tearDown(self):
    # Cleaning up the Steam directory should clean up anything that the user
    # fixture added
    self.steam_fixture.tearDown()

  def _create_default_directories(self):
    """This method creates all of the directories that Steam normally creates
    for a user."""
    # Assert that the userdata directory is there
    assert(os.path.exists(self.steam_fixture.get_steam().userdata_directory))
    # The data directory for our user, which acts as the root of userdata
    # hierarchy
    os.mkdir(paths.user_specific_data_directory(self.get_context()))
    # The "config" directory, which stores shortcuts.vdf and the grid directory
    # TODO: There should probably be a helper function for this in pysteam
    os.mkdir(os.path.join(paths.user_specific_data_directory(self.get_context()), "config"))
    # The directory which stores grid images
    os.mkdir(paths.custom_images_directory(self.get_context()))

  def get_user_id(self):
    return self.uid

  def get_context(self):
    return model.LocalUserContext(self.steam_fixture.get_steam(), self.uid)
