from dataclasses import dataclass

from Api import data
from Api.recipes.component_filters import ComponentFilters
from Api.recipes.ingredient_slot import IngredientSlot
from Api.recipes.recipe import Recipe


@dataclass
class RecipesDefault:
    modeling = Recipe(ingredient_slots=[
        IngredientSlot(name='Extra', multiple=True, filters=[]),
    ])

    rigging = Recipe(ingredient_slots=[
        IngredientSlot(name='Geos', multiple=True, filters=[ComponentFilters.Component(items=[data.Components.geo])]),
        IngredientSlot(name='Extra', multiple=True, filters=[]),
    ])

    texturing = Recipe(ingredient_slots=[
        IngredientSlot(name='Geo', multiple=False, filters=[ComponentFilters.Component(items=[data.Components.geo])]),
    ])

    shading = Recipe(ingredient_slots=[
        IngredientSlot(name='Geo', multiple=False, filters=[ComponentFilters.Component(items=[data.Components.geo])]),
    ])

    animation = Recipe(ingredient_slots=[
        IngredientSlot(name='CamRig', multiple=False, filters=[ComponentFilters.Component(items=[data.Components.cam_rig])]),
        IngredientSlot(name='Decor', multiple=False, filters=[ComponentFilters.Category(items=[data.Categories.decor])]),
        IngredientSlot(name='Rigs', multiple=True, filters=[ComponentFilters.Component(items=[data.Components.rig])]),
        IngredientSlot(name='Extra', multiple=True, filters=[]),
    ])

    lighting = Recipe(ingredient_slots=[
        IngredientSlot(name='Cam', multiple=False, filters=[ComponentFilters.Component(items=[data.Components.cam])]),
        IngredientSlot(name='Animated', multiple=True, filters=[ComponentFilters.Component(items=[data.Components.anim])]),
        IngredientSlot(name='Static', multiple=True, filters=[ComponentFilters.Component(items=[data.Components.shd])]),
        IngredientSlot(name='Extra', multiple=True, filters=[]),
    ])
