# encoding: utf-8

from error import HumanReadableError
from logs import logger

def catch_exceptions(handler):
  def decorator(func):
    def wrapped(*args, **kwargs):
      try:
        func(*args, **kwargs)
      except HumanReadableError as hre:
        handler(hre, fatal = False)
      except Exception as e:
        handler(e, fatal = True)
    return wrapped
  return decorator
