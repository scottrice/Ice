
import os
import unicodedata

class ROMParser(object):
  def __init__(self, logger):
    self.logger = logger

  def parse(self, path):
    """Parses the name of the ROM given its filename."""
    name_with_ext = os.path.basename(path)

    # normalize the name to get rid of symbols that break the shortcuts.vdf
    name_with_ext = unicodedata.normalize(
        'NFKD', unicode(name_with_ext.decode('utf-8'))).encode('ascii', 'ignore')

    dot_index = name_with_ext.rfind('.')
    if dot_index == -1:
      # There is no period, so there is no extension. Therefore, the
      # name with extension is the name
      return name_with_ext
    # Return the entire string leading up to (but not including) the period
    return name_with_ext[:dot_index]
