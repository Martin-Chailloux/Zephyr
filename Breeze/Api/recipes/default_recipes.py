from dataclasses import dataclass

from Api import data
from Api.recipes.component_filters import ComponentFilters
from Api.recipes.ingredient_slot import IngredientSlot
from Api.recipes.recipe import Recipe


@dataclass
class RecipesDefault:
    modeling = Recipe(ingredient_slots=[
        IngredientSlot(name='extra', multiple=True, filters=[]),
    ])

    rigging = Recipe(ingredient_slots=[
        IngredientSlot(name='geo', multiple=True, filters=[ComponentFilters.Component(items=[data.Components.geo])]),
        IngredientSlot(name='extra', multiple=True, filters=[]),
    ])

    texturing = Recipe(ingredient_slots=[
        IngredientSlot(name='geo', multiple=False, filters=[ComponentFilters.Component(items=[data.Components.geo])]),
    ])

    shading = Recipe(ingredient_slots=[
        IngredientSlot(name='geo', multiple=False, filters=[ComponentFilters.Component(items=[data.Components.geo])]),
    ])

    animation = Recipe(ingredient_slots=[
        IngredientSlot(name='camrig', multiple=False, filters=[ComponentFilters.Component(items=[data.Components.cam_rig])]),
        IngredientSlot(name='decor', multiple=False, filters=[ComponentFilters.Category(items=[data.Categories.decor])]),
        IngredientSlot(name='rig', multiple=True, filters=[ComponentFilters.Component(items=[data.Components.rig])]),
        IngredientSlot(name='extra', multiple=True, filters=[]),
    ])

    lighting = Recipe(ingredient_slots=[
        IngredientSlot(name='cam', multiple=False, filters=[ComponentFilters.Component(items=[data.Components.cam])]),
        IngredientSlot(name='animated', multiple=True, filters=[ComponentFilters.Component(items=[data.Components.anim])]),
        IngredientSlot(name='static', multiple=True, filters=[ComponentFilters.Component(items=[data.Components.shd])]),
        IngredientSlot(name='extra', multiple=True, filters=[]),
    ])
