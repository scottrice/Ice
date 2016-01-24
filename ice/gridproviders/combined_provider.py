# encoding: utf-8

from functools import reduce

import grid_image_provider

from ice.logs import logger

class CombinedProvider(grid_image_provider.GridImageProvider):

  def __init__(self, *args):
    """
    Creates a CombinedProvider out of the providers that were passed in `args`

    ORDER MATTERS. `image_for_rom` will return the first non-None result from
    a provider. So if you want to check the users filesystem but check
    ConsoleGrid if nothing is found then you would do

    CombinedProvider(LocalProvider(), ConsoleGridProvider())

    But if you wanted to, say, use ConsoleGrid but show a placeholder image in
    the case of an error you would do

    CombinedProvider(ConsoleGridProvider(), PlaceholderProvider())
    """
    self.providers = args

  def _enabled_providers(self):
    return filter(lambda provider: provider.is_enabled(), self.providers)

  def is_enabled(self):
    """
    Returns True if any child provider is enabled
    """
    return len(self._enabled_providers()) > 0

  def image_for_rom(self, rom):
    """
    Returns the first image found
    """
    return reduce(lambda image, provider: image if image else provider.image_for_rom(
        rom), self._enabled_providers(), None)
