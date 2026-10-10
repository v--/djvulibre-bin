project(
    'djvulibre-bin',
    'cpp',
    meson_version: '>=1.1.0'
)

cpp = meson.get_compiler('cpp')
libdjvu_dep = cpp.find_library('djvulibre', required: false, dirs: [
    join_paths(meson.project_source_root(), get_option('os'), get_option('cpu_family'), get_option('djvulibre_version'))
])

if not libdjvu_dep.found()
    error('Could not load libdjvulibre version ' + get_option('djvulibre_version') + ' for ' + get_option('cpu_family') + ' on ' + get_option('os'))
endif
