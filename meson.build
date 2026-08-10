project(
    'djvulibre-bin',
    'cpp'
)

cpp = meson.get_compiler('cpp')
libdjvu_dep = cpp.find_library('djvulibre', dirs: [
    join_paths(meson.project_source_root(), 'windows', get_option('djvulibre_version'), get_option('cpu_family'))
])
