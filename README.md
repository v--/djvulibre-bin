# DjVuLibre binaries

This repository contains precompiled `libdjvulibre` from [DjVuLibre](https://djvu.sourceforge.net/) for platforms like Windows on x86_64 that are not officially supported (but seem to work fine as-is). I did not manage to get aarch64 cross-compilation to work.

These files are intended to be used by [python-djvulibre-ng](https://github.com/v--/python-djvulibre-ng).

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
