# encoding: utf-8

from logs import logger

def catch_exceptions(msg):
  def decorator(func):
    def wrapped(*args, **kwargs):
      try:
        func(*args, **kwargs)
      except Exception as e:
        logger.exception(msg)
    return wrapped
  return decorator
