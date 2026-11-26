from pythonforandroid.recipe import PythonRecipe


class MaterialyoucolorRecipe(PythonRecipe):
    version = '3.0.4'
    url = 'https://github.com/T-Dynamos/materialyoucolor-python/releases/download/v{version}/materialyoucolor-{version}.tar.gz'
    depends = ['pillow']
    site_packages_name = 'materialyoucolor'
    call_hostpython_via_targetpython = False
    setup_extra_args = ['--no-deps']

    def get_recipe_env(self, arch, **kwargs):
        env = super().get_recipe_env(arch, **kwargs)
        env['MYCP_PURE_PYTHON'] = '1'
        return env


recipe = MaterialyoucolorRecipe()
