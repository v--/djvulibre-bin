import os
import pathlib
import re
import sysconfig
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class DjVuLibreBuildError(Exception):
    pass


class CustomBuildHook(BuildHookInterface):
    def extract_platform_tag(self) -> str:
        if override := os.environ.get('DJVULIBRE_PLATFORM_TAG'):
            return override

        return sysconfig.get_platform().replace('-', '_')

    def extract_djvulibre_version(self) -> str:
        return re.sub(r'(\.post\d+)$', '', self.metadata.core.version)

    def get_bin_root_path(self) -> pathlib.Path:
        build_root = pathlib.Path(__file__).parent
        return build_root / 'bin'

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        if version != 'standard':
            raise DjVuLibreBuildError(f'Unsupported hatchling build version {version!r}')

        build_data['pure_python'] = False

        platform_tag = self.extract_platform_tag()

        if platform_tag != 'win_amd64':
            raise DjVuLibreBuildError(f'Unsupported platform with tag {platform_tag}')

        build_data['tag'] = f'py3-none-{platform_tag}'
        djvulibre_version = self.extract_djvulibre_version()

        bin_path = self.get_bin_root_path() / 'windows' / 'x86_64' / djvulibre_version

        if not bin_path.exists():
            raise DjVuLibreBuildError(f'Unsupported DjVuLibre version {djvulibre_version} for {platform_tag}')

        build_data['force_include'] = {str(bin_path): 'djvulibre_bin/bin'}
