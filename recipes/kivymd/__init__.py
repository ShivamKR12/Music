import glob
import os
import shutil
from pythonforandroid.recipe import PythonRecipe


class KivyMDRecipe(PythonRecipe):
    version = '2.0.0'
    url = 'https://github.com/kivymd/KivyMD/archive/refs/tags/{version}.zip'
    depends = ['kivy', 'materialyoucolor', 'asynckivy', 'pillow']
    site_packages_name = 'kivymd'
    call_hostpython_via_targetpython = False
    setup_extra_args = ['--no-deps']

    def prebuild_arch(self, arch):
        super().prebuild_arch(arch)
        build_dir = self.get_build_dir(arch.arch)
        setup_file = os.path.join(build_dir, 'setup.py')
        if os.path.exists(setup_file):
            with open(setup_file, 'r', encoding='utf-8') as f:
                content = f.read()
            broken_line = 'filepath = os.path.join(\n                    str(Path(*Path(root).parts[1:])), file\n                )'
            broken_line_alt = 'filepath = os.path.join(str(Path(*Path(root).parts[1:])), file)'
            fixed_block = """rel_dir = os.path.relpath(root, src_path)
                if rel_dir == '.':
                    filepath = file
                else:
                    filepath = os.path.join(rel_dir, file).replace('\\\\', '/')"""
            if broken_line in content:
                content = content.replace(broken_line, fixed_block)
            elif broken_line_alt in content:
                content = content.replace(broken_line_alt, fixed_block)
            with open(setup_file, 'w', encoding='utf-8') as f:
                f.write(content)

    def postbuild_arch(self, arch):
        super().postbuild_arch(arch)
        # Ensure all package data (.kv, .json, .png, .atlas, .ttf, .glsl) are copied to site-packages
        src_dir = os.path.join(self.get_build_dir(arch.arch), 'kivymd')
        dest_dir = os.path.join(self.ctx.get_site_packages_dir(arch), 'kivymd')
        if os.path.exists(src_dir) and os.path.exists(dest_dir):
            for ext in ('*.kv', '*.json', '*.png', '*.atlas', '*.ttf', '*.glsl'):
                for src_path in glob.glob(os.path.join(src_dir, '**', ext), recursive=True):
                    rel_path = os.path.relpath(src_path, src_dir)
                    dest_path = os.path.join(dest_dir, rel_path)
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    if not os.path.exists(dest_path):
                        shutil.copy2(src_path, dest_path)


recipe = KivyMDRecipe()
