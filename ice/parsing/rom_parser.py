
import os
import re
import unicodedata

from ice.logs import logger

class ROMParser(object):

  regexes = [
    # Regex that matches the entire string up until it hits the first '[',
    # ']', '(', ')', or '.'
    # DOESN'T WORK FOR GAMES WITH ()s IN THEIR NAME
    ur"(?P<name>[^\(\)\[\]]*).*",
  ]

  def __init__(self):
    logger.debug("Creating ROM parser with regexes: %s" % self.regexes)

  def parse(self, path):
    """Parses the name of the ROM given its path."""
    basename = os.path.basename(path)
    (filename, ext) = os.path.splitext(basename)
    opts = re.IGNORECASE
    match = reduce(lambda match, regex: match if match else re.match(regex, filename, opts), self.regexes, None)
    if match:
      logger.debug("Matched game '%s' as %s using regular expression `%s`", filename, str(match.groupdict()), match.re.pattern)
      name = match.groupdict()["name"]
    else:
      logger.debug("No match found for '%s'", filename)
      name = filename
    return name.strip()
