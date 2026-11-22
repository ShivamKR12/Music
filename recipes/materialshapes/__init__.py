from pythonforandroid.recipe import Recipe


class MaterialShapesRecipe(Recipe):
    """Dummy recipe for materialshapes to satisfy any requirements check without compiling pycairo."""
    depends = []

    def should_be_built(self, arch):
        return False


recipe = MaterialShapesRecipe()
