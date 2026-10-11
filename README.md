# DjVuLibre binaries

This repository contains precompiled `libdjvulibre` from [DjVuLibre](https://djvu.sourceforge.net/) for platforms like Windows on x86_64 that are not officially supported (but seem to work fine as-is). I did not manage to get aarch64 cross-compilation to work.

The precompiled files in [`./bin`](./bin) are intended to be used by [python-djvulibre-ng](https://github.com/v--/python-djvulibre-ng). Please let me know if your project depends on them so that I can be more careful with backward compatibility.

## Usage

### Meson

I initially planned to use Meson's [wrap dependency system](https://mesonbuild.com/Wrap-dependency-system-manual.html) to install this package where appropriate. See [this commit](https://github.com/v--/python-djvulibre-ng/blob/b9a8fb8f4afc8b3e6cf1e7865da35e9f6dc74615/src/djvulibre/meson.build) for a successful setup with [pybind11](https://pybind11.readthedocs.io).

### Python

I decided to provide a Python module specifically for FFI-based bindings. It can be installed as follows:

```toml
"djvulibre-bin @ git+https://github.com/v--/djvulibre-bin.git@v{version} ; os_name=='nt'"
```

See the [`api.py`](./src/djvulibre_bin/api.py) for library loading helpers.

> [!NOTE]
> Only the wheel builds properly expose the binaries. Source distributions and editable are not expected to work.

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

For each configuration, I simply build `libdjvulibre` and copy the `.dll` file into the corresponding directory.
