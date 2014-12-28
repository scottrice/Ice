
import glob
import os


class Filesystem(object):

  def path_exists(self, path):
    return os.path.exists(path)

  def is_directory(self, path):
    assert self.path_exists(
        path), "`is_directory` expects the given path to exist"
    return os.path.isdir(path)

  def _paths_in_directory(self, directory):
    assert self.is_directory(
        directory), "`paths_in_directory` expects a directory parameter"
    # Use glob instead of `os.listdir` to find files because glob will ignore
    # hidden files. Or at least some hidden files. It ignores any file whose
    # name starts with ".", which is basically equivalent to 'hidden files' on
    # OSX/Linux, but means nothing on Windows. Still, its good enough, and I'd
    # like to avoid having OS-specific 'ignore hidden files' logic in this file
    # and let Python handle it instead.
    pattern = os.path.join(directory, "*")
    return [os.path.join(directory, name) for name in glob.glob(pattern)]

  def files_in_directory(self, directory):
    return filter(os.path.isfile, self._paths_in_directory(directory))

  def subdirectories_of_directory(self, directory):
    return filter(os.path.isdir, self._paths_in_directory(directory))
