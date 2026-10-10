"""A simple API for retrieving the path of libdjvulibre."""

import importlib.resources.abc


def get_libdjvulibre_resource(os: str, cpu_family: str, soname_version: int) -> importlib.resources.abc.Traversable:
    if os != 'nt' and os != 'windows':
        raise OSError(f'Unsupported OS {os!r}')

    normalized_os = 'windows'

    if cpu_family != 'AMD64' and cpu_family != 'x86_64':
        raise OSError(f'Unsupported CPU family {cpu_family!r}')

    normalized_cpu_family = 'x86_64'

    if soname_version != 21:
        raise OSError(f'Unsupported soname with version {soname_version!r}')

    djvulibre_version = '3.5.30.1'
    return importlib.resources.files("djvulibre-bin") / normalized_os / normalized_cpu_family / djvulibre_version / 'libdjvulibre'
