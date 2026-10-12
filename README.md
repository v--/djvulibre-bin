# DjVuLibre binaries

This repository contains precompiled `libdjvulibre` from [DjVuLibre](https://djvu.sourceforge.net/) for platforms like Windows on x86_64 that are not officially supported (but seem to work fine as-is). I did not manage to get aarch64 cross-compilation to work.

The precompiled files in [`./bin`](./bin) are intended for [python-djvulibre-ng](https://github.com/v--/python-djvulibre-ng). They should be immutable. Please let me know if your project depends on them so that I can be more careful with backward compatibility.

## Meson usage

I initially planned to use Meson's [wrap dependency system](https://mesonbuild.com/Wrap-dependency-system-manual.html) to install this package where appropriate. See [this commit](https://github.com/v--/python-djvulibre-ng/blob/b9a8fb8f4afc8b3e6cf1e7865da35e9f6dc74615/src/djvulibre/meson.build) for a working setup with [pybind11](https://pybind11.readthedocs.io).

### Python usage

The binaries are packages into Python wheels specifically for FFI-based bindings.

The `djvulibre_bin` module provides a `LIBDJVULIBRE_RESOURCE_DIRECTORY` [`Traversable`](https://docs.python.org/3/library/importlib.resources.abc.html#importlib.resources.abc.Traversable) constant, which can be used as follows:

```python
with importlib.resources.as_file(LIBDJVULIBRE_RESOURCE_DIRECTORY / 'libdjvulibre') as path:
    return ctypes.CDLL(str(path))
```

### Installation from wheels

I wanted to avoid hosting these files on a packaging index, so I use the repository itself to host wheels in [`dist/`](./dist/).

A particular `version` has the format `{djvulibre_version}.post{revision}` and can be added as a dependency using the following [specifier](https://packaging.python.org/en/latest/specifications/dependency-specifiers/):

```plain
djvulibre-bin @ https://github.com/v--/djvulibre-bin/raw/refs/heads/master/dist/djvulibre_bin-{version}-py3-none-win_amd64.whl ; sys_platform=='win32' and platform_machine=='AMD64'
```

Naturally, the wheels are supposed to be immutable. You can pin a commit rather than the master branch.

### Installation from source

Alternatively, you can install from source:

```plain
djvulibre-bin @ git+https://github.com/v--/djvulibre-bin ; sys_platform=='win32'
```

### Building the wheels

The wheels are built via a [hatch plugin](./hatch_build.py). The build itself follows the [PEP 517](https://peps.python.org/pep-0517/) standard and the platform can be configured with an environment variable:

```shell
DJVULIBRE_PLATFORM_TAG=win_amd64 python -m build --wheel
```

> [!WARNING]
> Building the same wheel on Windows and Unix may result in different files due to CRLF differences.

> [!NOTE]
> The source distribution simply includes all binaries, while editable installs are disallowed by the hatch plugin.

## libdjvulibre build process

This is a rough description of the build process I have used. It would perhaps be easy to automate if Visual Studio was not involved.

### Initially setting up the DjVuLibre repository

Download the code and make sure to use the latest tag of each dependency.

```powershell
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

git clone https://git.code.sf.net/p/djvu/djvulibre-git djvulibre
cd djvulibre
git checkout $(git describe --tags --abbrev=0)

cd jpeg
Invoke-WebRequest https://sourceforge.net/projects/libjpeg/files/libjpeg/6b/jpegsrc.v6b.tar.gz -OutFile jpegsrc.v6b.tar.gz
tar xf jpegsrc.v6b.tar.gz
cd ..

cd tiff
git clone https://gitlab.com/libtiff/libtiff
cd libtiff
git checkout $(git describe --tags --abbrev=0)
cd ..
New-Item -Path tiff -ItemType SymbolicLink -Value libtiff

cd zlib
git clone https://github.com/madler/zlib
cd zlib
git checkout $(git describe --tags --abbrev=0)
cd ..
```

### Adding build configurations

In Visual Studio, I manually add build configurations for architectures like x86_64. This further requires installing build tools and platform dependencies from the Visual Studio Installer.

### Building

For each configuration, I simply build `libdjvulibre` and copy the `libdjvulibre.dll` and `libjpeg.dll` files into the corresponding directory.
