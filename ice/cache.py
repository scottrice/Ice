
class Cache(object):

  def __init__(self):
    self.__store__ = {}

  def get(self, *args):
    if len(args) is 0:
      raise StandardError("Must provide at least one key to `cache.get()`")

    key = args[0]

    # Easy case
    if key not in self.__store__:
      return None

    # This is our only key, just return whatever we've got
    if len(args) is 1:
      # This is the only key, return it from storage
      return self.__store__.get(key)

    # More than one argument, get the next cache one level down and return its
    # value for the remaining arguments
    subcache = self.__store__[key]
    if not isinstance(subcache, Cache):
      raise StandardError("Attempting to get value from multi level cache "
                          "after explicitly setting intermediate value")

    # If we were called with `get(a, b, c)`, `return subcache.get(b, c)`
    return subcache.get(*args[1:])

  def set(self, *args):
    if len(args) < 2:
      raise StandardError("Must provide at least a key and a value to "
                          "`cache.set()`")

    key = args[0]

    # Base case - standard caching. Set the key to the value
    if len(args) is 2:
      value = args[1]
      self.__store__[key] = value
      return

    # More interesting case - if we have a subcache, use it. Otherwise, create
    # a new instance
    if key not in self.__store__ or not isinstance(self.__store__[key], Cache):
      self.__store__[key] = Cache()

    subcache = self.__store__[key]
    subcache.set(*args[1:])
