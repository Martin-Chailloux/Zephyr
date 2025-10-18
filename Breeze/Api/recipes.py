from dataclasses import dataclass
from typing import Any

from Api.project_documents import Component, Version
from Api.studio_documents import StageTemplate
from Gui.popups.component_browser import ComponentBrowser



class ComponentFilterBase:
    name: str

    def __init__(self, items: list[str], exclude: bool=False):
        self.items = [s.lower() for s in items]
        self.exclude = exclude

    def get_filtered_components(self, components: list[Component]) -> list[Component]:
        pass

    def to_dict(self):
        result = {'items': self.items, 'exclude': self.exclude}
        return result


class ComponentFilterCategory(ComponentFilterBase):
    filter_type = 'category'
    def get_filtered_components(self, components: list[Component]) -> list[Component]:
        input_components = components
        components = [c for c in components if c.stage.asset.category.lower() in self.items]
        if self.exclude:  # TODO: call a method in upperclass instead
            components = [c for c in input_components if c not in components]
        return components


class ComponentFilterStage(ComponentFilterBase):
    name = 'stage'
    def get_filtered_components(self, components: list[Component]) -> list[Component]:
        input_components = components
        components = [c for c in components if c.stage.stage_template.label.lower() in self.items]
        if self.exclude:
            components = [c for c in input_components if c not in components]
        return components


@dataclass
class ComponentFilters:
    category = ComponentFilterCategory
    stage = ComponentFilterStage


class IngredientSlot:
    def __init__(self, name: str, multiple: bool = False, filters: list[ComponentFilterBase] = None):
        """
        :param name (str): name of the slot
        :param multiple (bool): can receive multiple ingredients
        :param filters (list[ComponentFilterBase]): pre-filters the available components
        """
        self.name = name
        self.is_multiple = multiple
        self.filters: list[ComponentFilterBase] = filters or []

        self.allowed_components = self.get_allowed_components()
        # self.show_select_popup()

    def get_allowed_components(self) -> list[Component]:
        components: list[Component] = Component.objects
        for component_filter in self.filters:
            components = component_filter.get_filtered_components(components=components)
        return components

    def show_select_popup(self):
        browser = ComponentBrowser(components=self.allowed_components)
        browser.show_menu([0.5, 0.5])

    def to_database(self) -> dict[str, Any]:
        infos: dict[str, Any] = {
            "name": self.name,
            "multiple": self.is_multiple,
            "filters": {},  # dict[name, ComponentFilterBase.to_dict()]
        }
        for component_filter in self.filters:
            infos['filters'][component_filter.name] = component_filter.to_dict()
        return infos

    @classmethod
    def from_database(cls, infos: dict[str, Any]):
        name = infos['name']
        multiple = infos['multiple']

        # get filters
        filters: list[ComponentFilterBase] = []
        for filter_name, filter_infos in infos['filters'].items():
            items = filter_infos['items']
            exclude = filter_infos['exclude']
            if filter_name == ComponentFilters.category:
                filters.append(ComponentFilterCategory(items=items, exclude=exclude))
            elif filter_name == ComponentFilters.stage:
                filters.append(ComponentFilterStage(items=items, exclude=exclude))

        ingredient = cls(name=name, multiple=multiple, filters=filters)
        # ingredient.set_version(version)  # note: this will also set the component
        return ingredient

    def add_to_stage_template(self, stage_template: StageTemplate):
        recipe = Recipe.from_database(recipe_infos=stage_template.recipe)
        recipe.add_ingredient(ingredient=self)
        stage_template.recipe = recipe.to_database()
        stage_template.save()
        print(f"Added ingredient slot to {stage_template}: {self.to_database()}")


class Ingredients:
    def __init__(self, name: str, versions: list[Version]):
        self.name = name
        self.versions = versions

    def to_database(self) -> dict[str, Any]:
        result = {'name': self.name, 'versions': self.versions}
        return result

    @classmethod
    def from_database(cls, ingredient_infos: dict[str, Any]):
        name = ingredient_infos['name']
        versions = ingredient_infos['versions']
        return cls(name=name, versions=versions)


class Recipe:
    def __init__(self, ingredients: list[IngredientSlot]):
        self.ingredients_slots = ingredients

    def to_database(self) -> list[dict[str, Any]]:
        ingredients: list[dict[str, Any]] = [ingredient_slot.to_database() for ingredient_slot in self.ingredients_slots]
        return ingredients

    @classmethod
    def from_database(cls, recipe_infos: list[dict[str, Any]]):
        ingredients: list[IngredientSlot] = []
        for ingredient_infos in recipe_infos:
            ingredients.append(IngredientSlot.from_database(infos=ingredient_infos))
        return cls(ingredients=ingredients)

    def add_ingredient(self, ingredient: IngredientSlot):
        names = [ingredient.name for ingredient in self.ingredients_slots]
        if ingredient.name in names:
            raise ValueError(f"This recipe already contains an ingredient with name: {ingredient.name}")
        self.ingredients_slots.append(ingredient)
