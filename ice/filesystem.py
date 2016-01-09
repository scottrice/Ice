
import glob
import os


class RealFilesystem(object):

  def create_directories(self, path):
    return os.makedirs(path)

  def path_exists(self, path):
    return os.path.exists(path)

  def is_directory(self, path):
    return os.path.isdir(path)

  def is_file(self, path):
    return os.path.isfile(path)

  def is_writable(self, path):
    return os.access(path, os.W_OK)

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
    return filter(
      os.path.isfile,
      self._paths_in_directory(directory, incl_subdirs=include_subdirectories),
    )

  def subdirectories_of_directory(self, directory, recursive=False):
    assert self.is_directory(directory), "Must specify a directory"
    return filter(
      os.path.isdir,
      self._paths_in_directory(directory, incl_subdirs=recursive),
    )

class FakeFilesystem(object):

  def __init__(self, root):
    self.root = root

    self.fs = RealFilesystem()

  def adjusted_path(self, path):
    """Adjusts the parameter `path` to be rooted in self.root rather than in
    the current directory (or the specified directory, if given)"""
    # Check if path is already a subdirectory of the root. If it is, then we
    # don't need to do any adjusting
    if os.path.realpath(path).startswith(os.path.realpath(self.root)):
      return path
    # Unfortunately we can't just use `os.path.join` here, as doing so when
    # `path` is absoulte simply returns `path`.
    to_components = lambda p: os.path.normpath(p).split(os.sep)
    root_components = to_components(self.root)
    path_components = to_components(path)

    # If the parameter path is absolute, it's components array will contain
    # some marker that it is absolute (a drive identifier on Windows, and an
    # empty component on Posix). By removing the first component we turn it
    # into a relative path which can be appended to the root.
    if os.path.isabs(path):
      path_components.pop(0)
    return os.sep.join(root_components + path_components)

  def create_directories(self, path):
    return self.fs.create_directories(self.adjusted_path(path))

  def path_exists(self, path):
    return self.fs.path_exists(self.adjusted_path(path))

  def is_directory(self, path):
    return self.fs.is_directory(self.adjusted_path(path))

  def is_file(self, path):
    return self.fs.is_file(self.adjusted_path(path))

  def is_writable(self, path):
    return self.fs.is_writable(self.adjusted_path(path))

  def files_in_directory(self, directory, include_subdirectories=False):
    return self.fs.files_in_directory(
      self.adjusted_path(directory),
      include_subdirectories=include_subdirectories
    )

  def subdirectories_of_directory(self, directory, recursive=False):
    return self.fs.files_in_directory(
      self.adjusted_path(directory),
      recursive=recursive
    )