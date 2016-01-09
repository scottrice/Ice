
import collections
import json
import os
import shutil
import tempfile
import traceback

from functools import partial
from pysteam import model
from pysteam import paths
from pysteam import shortcuts

from ice.configuration import Configuration
from ice.filesystem import FakeFilesystem
from ice.persistence.config_file_backing_store import ConfigFileBackingStore
from ice.runners.command_line_runner import CommandLineRunner

from fixtures import SteamFixture, UserFixture

class FakeEnvironment(object):
  def __init__(self, file_path):
    """
    Generates a new environment in which to run Integration tests.
    `testdata_dir` refers to the base testdata directory, which individual tests
    will then use to load their test-specific configurations.
    """
    # We also need a sandbox to play in.
    self.sandbox = FakeFilesystem(root = tempfile.mkdtemp())
    # Need a dummy Steam installation for Ice to work with
    # We'll put it in the `Steam` directory of our sandbox
    self.steam_fixture = SteamFixture(os.path.join(self.sandbox.root, "Steam"))
    # Create a list of user fixtures that consumers can populate
    self.user_fixtures = []
    # The testdata directory should be in the same directory as the tests
    # themselves.
    self.testdata_dir = os.path.join(os.path.dirname(file_path), "testdata")
    assert(os.path.exists(self.testdata_dir))

    self.loaded_data = None
    self.extra_args = []

  def clean(self):
    for user_fixture in self.user_fixtures:
      user_fixture.tearDown()
    self.steam_fixture.tearDown()
    shutil.rmtree(self.sandbox.root)

  def _use_config_file(self, file, location):
    assert(os.path.exists(location))
    self.extra_args.append('--%s' % file)
    self.extra_args.append(location)

  def _test_config_path(self, directory, file):
    return os.path.join(directory, '%s.txt' % file)

  def _load_config_file_overrides(self, directory):
    file_basenames = ['config', 'consoles', 'emulators']
    filenames = map(lambda f: '%s.txt' % f, file_basenames)
    for f in file_basenames:
      self._use_config_file(f, self._test_config_path(directory, f))

  def _load_roms_for_test(self, directory):
    """Takes the ROMs located in `directory/ROMs` and moves them into the
    ROMs directory specified in the provided config.txt file."""
    # TODO: This is extremely non-kosher. The fact that I have to do this
    # suggests that something is very wrong with my Configuration object.
    #
    # Knowing that object I'm tempted to agree.
    c = Configuration(
      ConfigFileBackingStore(self._test_config_path(directory, 'config')),
      None,
      None,
      None,
      None,
    )
    target_roms_directory = self.sandbox.adjusted_path(c.roms_directory())
    source_roms_directory = os.path.join(directory, 'ROMs')
    shutil.copytree(source_roms_directory, target_roms_directory)

  def _override_backups_directory(self, data_directory):
    # TODO: Figure out a way to actually override this, so I can test that
    # backups get made correctly.
    pass

  def _adjust_json_path(self, path):
    return path.replace("%sb", self.sandbox.root)

  def _shortcut_from_expectation_json(self, json):
    for field in ["name", "exe", "startdir", "icon", "tags"]:
      assert(field in json)
    return model.Shortcut(
      name = json.get("name"),
      exe = self._adjust_json_path(json.get("exe")),
      startdir = json.get("startdir"),
      icon = json.get("icon"),
      tags = json.get("tags")
    )

  def load_test_data(self, testdata):
    """
    Reads the config.txt, consoles.txt, emulators.txt, shortcuts.vdf, and ROMs
    folder from the provided testdata subdirectory and places it in the sandbox
    such that it will be used by Ice the next time its run.
    """
    assert(self.loaded_data is None, "Can't load test data twice in a single test")
    self.loaded_data = testdata
    data_directory = os.path.join(self.testdata_dir, testdata)
    assert(os.path.exists(data_directory), "Can't load test data from a missing directory")
    self._load_config_file_overrides(data_directory)
    self._load_roms_for_test(data_directory)
    self._override_backups_directory(data_directory)

  def create_fake_user(self, uid=None):
    fixture = UserFixture(self.steam_fixture, uid)
    self.user_fixtures.append(fixture)
    return fixture.uid

  def expected_shortcuts(self):
    """Returns the shortcuts which the test expects will exist after executing"""
    expectations_path = os.path.join(self.testdata_dir, self.loaded_data, "shortcuts-expected.json")
    with open(expectations_path) as f:
      expected_shortcuts_json = json.load(f)
    expected_shortcuts = map(self._shortcut_from_expectation_json, expected_shortcuts_json)
    return expected_shortcuts

  def user_shortcuts(self, uid):
    context = model.LocalUserContext(self.steam_fixture.get_steam(), uid)
    return shortcuts.get_shortcuts(context)

  def run_command(self, *args):
    """"
    Runs the command specified by `args`, where doing
        run_command("list", "consoles", "--json")
    is equivalent to running the command
        ./ice.py list consoles --json
    """
    # Turn `args` into a list, like `sys.argv` represents them
    args = list(args)
    # Add the 'ice.py' at the beginning of the list, which `run` will then
    # promptly ignore
    args.insert(0, "ice.py")
    args.extend(self.extra_args)
    # Run the command
    try:
      runner = CommandLineRunner(self.steam_fixture.get_steam(), self.sandbox)
      runner.run(args)
      success = True
    except Exception as e:
      success = False
      print e
