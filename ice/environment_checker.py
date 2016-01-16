"""
EnvironmentChecker is responsible for making sure that the current environment
is one that Ice can safely run on.
"""

import os
import psutil
import sys

from error.path_existance_error import PathExistanceError
from error.process_running_error import ProcessRunningError
from error.writable_path_error import WritablePathError


class EnvironmentChecker(object):

  def __init__(self, filesystem):
    self.filesystem = filesystem

  def __enter__(self):
    self.requirement_errors = []
    return self

  def __exit__(self, type, value, tb):
    self.resolve_unment_requirements()

  def require_directory_exists(self, path):
    """
    Validate that a directory exists.

    An attempt will be made to create a directory if it is missing

    Validation will fail if a directory cant be created at that path
    or if a file already exists there
    """
    if not self.filesystem.is_directory(path):
      self.requirement_errors.append(PathExistanceError(self.filesystem, path))

  def require_writable_path(self, path):
    """
    Validate that a path is writable.

    Returns an error if the path doesn't exist or it isn't writable
    None otherwise
    """
    if not self.filesystem.is_writable(path):
      self.requirement_errors.append(WritablePathError(path))

  def require_program_not_running(self, program_name):
    """
    Validate that a program with the name `program_name` is not currently
    running on the users system.
    """
    for pid in psutil.pids():
      try:
        p = psutil.Process(pid)
        if p.name().lower().startswith(program_name.lower()):
          return self.requirement_errors.append(
              ProcessRunningError(p.name()))
      except Exception:
        continue

  def resolve_unment_requirements(self):
    """
    Attempts to resolve any added requirements that were unmet
    """
    for err in self.requirement_errors:
      err.resolve()
