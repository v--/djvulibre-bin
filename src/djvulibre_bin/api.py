"""A simple API for retrieving the path of libdjvulibre."""

import importlib.resources.abc


def get_latest_available_djvulibre_version(soversion: int) -> str:
    """Get the latest available version of DjVuLibre for the given ABI version ("soversion") of libdjvulibre.

    Args:
        soversion: A number indicating the desired ABI version of libdjvulibre.

    Returns:
        The dot-separated version of DjVuLibre (e.g. '3.5.30.1').

    Raises:
        OSError: If the `soversion` is unrecognized.
    """
    if soversion != 21:
        raise OSError(f'Unsupported soversion {soversion!r}')

    return '3.5.30.1'


def get_libdjvulibre_resource(os: str, cpu_family: str, djvulibre_version: str) -> importlib.resources.abc.Traversable:
    """Get an importlib Traversable pointing to a binary of libdjvulibre.

    Returns:
        os: A string indicating the desired operating system, e.g. 'nt' or 'windows'; refer to `sys.platform`.
        cpu_family: A string indicating the desired CPU architecture, e.g. 'x86_64'; refer to `platform.machine`.

    Raises:
        OSError: If the `os` or `cpu_family` are unrecognized.
    """
    if os != 'nt' and os != 'windows':
        raise OSError(f'Unsupported OS {os!r}')

    normalized_os = 'windows'

    if cpu_family != 'AMD64' and cpu_family != 'x86_64':
        raise OSError(f'Unsupported CPU family {cpu_family!r}')

    normalized_cpu_family = 'x86_64'
    return importlib.resources.files('djvulibre_bin') / 'bin' / normalized_os / normalized_cpu_family / djvulibre_version / 'libdjvulibre'
