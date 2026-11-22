from pythonforandroid.recipe import PythonRecipe


class KivyMDRecipe(PythonRecipe):
    version = '2.0.0'
    url = 'https://github.com/kivymd/KivyMD/archive/refs/tags/{version}.zip'
    depends = ['kivy', 'materialyoucolor', 'asynckivy', 'pillow']
    site_packages_name = 'kivymd'
    call_hostpython_via_targetpython = False
    setup_extra_args = ['--no-deps']


recipe = KivyMDRecipe()
