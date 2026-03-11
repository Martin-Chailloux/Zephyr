from dataclasses import dataclass

from Breeze.Api import data
from Breeze.Api.recipes.component_filters import ComponentFilters
from Breeze.Api.recipes.ingredient_slot import IngredientSlot
from Breeze.Api.recipes.recipe import Recipe


@dataclass
class OutputDefaults:
    modeling = [data.Components.geo]
    rigging = [data.Components.rig]
    texturing = []
    shading = [data.Components.shd]
    animation = []
    lighting = []
