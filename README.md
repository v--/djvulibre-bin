# DjVuLibre binaries

This repository contains precompiled `libdjvulibre` from [DjVuLibre](https://djvu.sourceforge.net/) for platforms like Windows on x86_64 that are not officially supported (but seem to work fine as-is). I did not manage to get aarch64 cross-compilation to work.

The precompiled files in [`./bin`](./bin) are intended to be used by [python-djvulibre-ng](https://github.com/v--/python-djvulibre-ng). Please let me know if your project depends on them so that I can be more careful with backward compatibility.

## Usage

### Meson

I initially planned to use Meson's [wrap dependency system](https://mesonbuild.com/Wrap-dependency-system-manual.html) to install this package where appropriate. See [this commit](https://github.com/v--/python-djvulibre-ng/blob/b9a8fb8f4afc8b3e6cf1e7865da35e9f6dc74615/src/djvulibre/meson.build) for a successful setup with [pybind11](https://pybind11.readthedocs.io).

### Python

I decided to provide Python modules specifically for FFI-based bindings. A particular `version` has the format `{djvulibre_version}.post{revision}` and can be added as a dependency as follows:

```toml
"djvulibre-bin @ https://github.com/v--/djvulibre-bin/releases/download/v{version}/djvulibre_bin-{version}-any-none-win64.whl ; os_name=='nt'"


```

The wheels are built via a [hatch plugin](./hatch_plugin.py). The build itself follows the [PEP 517](https://peps.python.org/pep-0517/) standard and can be configured with environment variables:

```shell
DJVULIBRE_PLATFORM_TAG=win64 DJVULIBRE_VERSION=3.5.30.1 python -m build --wheel
```

> [!NOTE]
> The source distribution simply includes all binaries, while editable installs are disallowed by the hatch plugin.

The `djvulibre_bin` module provides a `LIBDJVULIBRE_RESOURCE_DIRECTORY` [`Traversable`](https://docs.python.org/3/library/importlib.resources.abc.html#importlib.resources.abc.Traversable) constant, which can be used as follows:

```python
with importlib.resources.as_file(LIBDJVULIBRE_RESOURCE_DIRECTORY / 'libdjvulibre') as path:
    return ctypes.CDLL(str(path))
```

## Build process

This is a rough description of the build process I have used. It would perhaps be easy to automate if Visual Studio was not involved.

### Initially setting up the repository

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
