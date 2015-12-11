from env_checker_error import EnvCheckerError


class ProcessRunningError(Exception):

  def __init__(self, process_name):
    self.process_name = process_name

  def resolve(self):
    raise EnvCheckerError(
        "`%s` cannot be running while Ice is being run" %
        self.process_name)
