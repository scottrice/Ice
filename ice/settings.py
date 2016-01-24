# encoding: utf-8

import os

import configuration
import paths

from logs import logger
from gridproviders.combined_provider import CombinedProvider
from gridproviders.consolegrid_provider import ConsoleGridProvider
from gridproviders.local_provider import LocalProvider
from persistence.backed_object_manager import BackedObjectManager
from persistence.config_file_backing_store import ConfigFileBackingStore
from persistence.adapters.console_adapter import ConsoleBackedObjectAdapter
from persistence.adapters.emulator_adapter import EmulatorBackedObjectAdapter

def find_settings_file(name, filesystem):
  """
  Returns the path to a data file named `filename`.
  This function first checks to see if the data file exists in the data
  directory. If so, it returns that.
  Then, this function checks to see if the data file exists in the local
  directory. If so, it returns that.
  If neither of those things are true then this function will return the
  path to a new file in the data directory.
  """
  local_path = os.path.abspath(name)
  data_path = paths.data_file_path(name)

  if filesystem.is_file(data_path):
    return data_path
  elif filesystem.is_file(local_path):
    return local_path
  else:
    return data_path

def settings_file_path(name, filesystem, override = None):
  if override is not None:
    return override
  return find_settings_file(name, filesystem)

def load_configuration(filesystem, override = None):
  path = settings_file_path('config.txt', filesystem, override)
  logger.debug("Loading config from path: %s" % path)
  return configuration.from_store(ConfigFileBackingStore(path))

def load_emulators(filesystem, override = None):
  path = settings_file_path('emulators.txt', filesystem, override)
  logger.debug("Loading emulators from path: %s" % path)
  return BackedObjectManager(
    ConfigFileBackingStore(path),
    EmulatorBackedObjectAdapter(filesystem)
  )

def load_consoles(emulators, filesystem, override = None):
  path = settings_file_path('consoles.txt', filesystem, override)
  logger.debug("Loading consoles from path: %s" % path)
  return BackedObjectManager(
    ConfigFileBackingStore(path),
    ConsoleBackedObjectAdapter(emulators)
  )

def image_provider(config):
  providerByName = {
    "local": LocalProvider,
    "consolegrid": ConsoleGridProvider,
  }
  normalize = lambda s: s.strip().lower()
  names = map(normalize, config.provider_spec.split(","))
  instances = map(lambda name: providerByName[name](), names)
  logger.debug("Creating with component providers: %s" % str(instances))
  if len(instances) == 0:
    logger.error("No image providers specified. Ice will run, but will not \
                  find grid images for your ROMs. If this wasnt intentional, \
                  see config.txt.")
  return CombinedProvider(*instances)
