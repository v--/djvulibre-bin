import importlib.resources


LIBDJVULIBRE_RESOURCE_DIRECTORY = importlib.resources.files('djvulibre_bin') / 'bin'


__all__ = ['LIBDJVULIBRE_RESOURCE_DIRECTORY']
