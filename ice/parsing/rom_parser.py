
import os
import re
import unicodedata

from ice.logs import logger

class ROMParser(object):

  regexes = [
    # Regex that matches the entire string up until it hits the first '[',
    # ']', '(', ')', or '.'
    # DOESN'T WORK FOR GAMES WITH ()s IN THEIR NAME
    ur"(?P<name>[^\(\)\[\]\.]*).*",
  ]

  def __init__(self):
    logger.debug("Creating ROM parser with regexes: %s" % self.regexes)

  def parse(self, path):
    """Parses the name of the ROM given its path."""
    filename = os.path.basename(path)
    opts = re.IGNORECASE
    match = reduce(lambda match, regex: match if match else re.match(regex, filename, opts), self.regexes, None)
    if match:
      logger.debug("[ROMParser] Matched game '%s' using regular expression `%s`", filename, match.re.pattern)
      name = match.groupdict()["name"]
    else:
      logger.debug("[ROMParser] No match found for '%s'", filename)
      name = filename
    return name.strip()
