# encoding: utf-8

import collections
import os
import random
import shutil
import tempfile

from pysteam import model as steam_model
from pysteam import paths

from ice import model
from ice import roms

class SteamFixture(object):
  def __init__(self, tempdir=None):
    self.tempdir = tempdir if tempdir is not None else tempfile.mkdtemp()

    # tempfile will make the directory I need, but if the tempdir was provided
    # we need to ensure that it exists
    if not os.path.exists(self.tempdir):
      os.makedirs(self.tempdir)

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
    return steam_model.Steam(self.tempdir)

class UserFixture(object):
  def __init__(self, steam_fixture, uid=None):
    self.steam_fixture = steam_fixture
    # No real special reasoning behind these numbers, just arbitrarys
    self.uid = uid if uid is not None else str(random.randint(5, 2000))
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
    return steam_model.LocalUserContext(self.steam_fixture.get_steam(), self.uid)

def DataFixture(data):
  """Creates a pseudo class out of the parameter dictionary `data`, and
  populates the object such that calling `object.foo` will return `bar` if the
  input dictionary has a key/value pair `"foo": "bar"`."""
  # Transform keys to remove invalid characters, like ` `.
  assert all([all([c.isalnum() or c=='_' for c in key]) for key in data.keys()]), "All dictionary keys must be valid python variable names"
  DataPseudoClass = collections.namedtuple('DataPseudoClass', data.keys())
  return DataPseudoClass(**data)

emulators = DataFixture({
  "mednafen": model.Emulator(
    name = 'Mednafen',
    location = '/emulators/Mednafen/mednafen',
    format = "%l %r"
  ),
})

consoles = DataFixture({
  "nes": model.Console(
    fullname = 'Nintendo Entertainment System',
    shortname = 'NES',
    extensions = 'nes',
    custom_roms_directory = '',
    prefix = '[NES]',
    icon = '/consoles/icons/nes.png',
    images_directory = '/consoles/grid/nes/',
    emulator = emulators.mednafen
  ),
  "snes": model.Console(
    fullname = 'Super Nintendo',
    shortname = 'SNES',
    extensions = 'snes',
    custom_roms_directory = '/external/consoles/roms/snes',
    prefix = '',
    icon = '/consoles/icons/snes.png',
    images_directory = '/consoles/grid/snes/',
    emulator = emulators.mednafen
  ),
  # HACK: We're cheating a bit here. For a tiny while Ice would automatically
  # add an extra category to shortcuts to let itself know whether it should be
  # responsibile for removing said shortcut if the exe went missing. We don't
  # do this anymore, but we may still want to test things which have the
  # special category attached. To work around this, we make a test console
  # with a fullname set to the flag, so that the automatically added category
  # has the flag tag.
  "flagged": model.Console(
    fullname = roms.ICE_FLAG_TAG,
    shortname = 'flagged',
    extensions = '',
    custom_roms_directory = '',
    prefix = '',
    icon = '',
    images_directory = '',
    emulator = emulators.mednafen,
  )
})

roms = DataFixture({
  "banjo_kazooie": model.ROM(
    name = 'Banjo Kazooie',
    path = '/roms/nes/Banjo Kazooie.nes',
    console = consoles.nes
  ),
  "contra": model.ROM(
    name = 'Contra',
    path = '/roms/nes/Contra.nes',
    console = consoles.nes
  ),
  "megaman": model.ROM(
    name = 'Megaman',
    path = '/roms/nes/Megaman.nes',
    console = consoles.nes
  ),
  "megamanx": model.ROM(
    name = 'Megaman X',
    path = '/roms/snes/Megaman X.snes',
    console = consoles.snes
  ),
})
