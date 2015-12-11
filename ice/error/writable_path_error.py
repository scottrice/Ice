from env_checker_error import EnvCheckerError


class WritablePathError(Exception):

  def __init__(self, path):
    self.path = path

  def resolve(self):
    # TODO: Actually attempt to resolve this?
    raise EnvCheckerError(
        "Ice requires write access too `%s` to run." %
        self.path)
