from dataclasses import dataclass

from Api import data
from Api.recipes.component_filters import ComponentFilters
from Api.recipes.ingredient_slot import IngredientSlot
from Api.recipes.recipe import Recipe


@dataclass
class OutputDefaults:
    modeling = [data.Components.geo]
    rigging = [data.Components.rig]
    texturing = []
    shading = [data.Components.shd]
    animation = []
    lighting = []
