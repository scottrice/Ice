import os

from ice.error.env_checker_error import EnvCheckerError


class PathExistanceError(Exception):

  def __init__(self, path):
    self.path = path

  def resolve(self):
    try:
      os.makedirs(self.path)
    except EnvironmentError as e:
      raise EnvCheckerError(
          "Could not create necessary directory `%s`" %
          self.path, self, e)
