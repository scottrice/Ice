
import glob
import os


class Filesystem(object):

  def path_exists(self, path):
    return os.path.exists(path)

  def is_directory(self, path):
    return os.path.isdir(path)

  def _paths_in_directory(self, directory, incl_subdirs=False):
    assert self.is_directory(directory)
    # Use glob instead of `os.listdir` to find files because glob will ignore
    # hidden files. Or at least some hidden files. It ignores any file whose
    # name starts with ".", which is basically equivalent to 'hidden files' on
    # OSX/Linux, but means nothing on Windows. Still, its good enough, and I'd
    # like to avoid having OS-specific 'ignore hidden files' logic in this file
    # and let Python handle it instead.
    pattern = os.path.join(directory, "*")
    result = glob.glob(pattern)
    # Unfortunately Python glob doesn't support `**` for matching 0 or 1
    # subdirectories (like I was hoping it would), so instead we run a second
    # glob if we need subdirectories
    subdir_pattern = os.path.join(directory, "*", "*")
    subdir_result = glob.glob(subdir_pattern) if incl_subdirs else []
    return result + subdir_result

  def files_in_directory(self, directory, include_subdirectories=False):
    assert self.is_directory(directory), "Must specify a directory"
    return self._paths_in_directory(directory, incl_subdirs=include_subdirectories)

  def subdirectories_of_directory(self, directory, recursive=False):
    assert self.is_directory(directory), "Must specify a directory"
    return filter(
      os.path.isdir,
      self._paths_in_directory(directory, incl_subdirs=recursive),
    )
