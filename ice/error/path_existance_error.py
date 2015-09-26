import os

from env_checker_error import EnvCheckerError


class PathExistanceError(Exception):

  def __init__(self, filesystem, path):
    self.filesystem = filesystem
    self.path = path

  def resolve(self):
    try:
      self.filesystem.create_directories(self.path)
    except EnvironmentError as e:
      raise EnvCheckerError(
          "Could not create necessary directory `%s`" %
          self.path, self, e)
