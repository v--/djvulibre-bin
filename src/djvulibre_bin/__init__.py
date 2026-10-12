import importlib.metadata
import importlib.resources
import re

LIBDJVULIBRE_VERSION = re.sub(r'(\.post\d+)$', '', importlib.metadata.version('djvulibre_bin'))
LIBDJVULIBRE_RESOURCE_DIRECTORY = importlib.resources.files('djvulibre_bin') / 'bin'


__all__ = ['LIBDJVULIBRE_RESOURCE_DIRECTORY', 'LIBDJVULIBRE_VERSION']
