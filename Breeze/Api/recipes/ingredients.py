from typing import Any

from Api.document_models.project_documents import Component, Version
from Api.recipes.component_filters import ComponentFilterBase, ComponentFilters


class IngredientSlot:
    def __init__(self, name: str, multiple: bool = False, filters: list[ComponentFilterBase] = None):
        """
        A template to receive ingredients, inside a Recipe.
        :param name: name of the slot
        :param multiple: can receive multiple ingredients
        :param filters: pre-filters the available components
        """
        self.name = name
        self.is_multiple = multiple
        self.filters: list[ComponentFilterBase] = filters or []

        self.allowed_components = self.get_allowed_components()

    def get_allowed_components(self) -> list[Component]:
        components: list[Component] = Component.objects
        for component_filter in self.filters:
            components = component_filter.get_filtered_components(components=components)
        return components

    def to_database(self) -> dict[str, Any]:
        infos: dict[str, Any] = {
            "multiple": self.is_multiple,
            "filters": {},  # dict[name, ComponentFilterBase.to_dict()]
        }
        for component_filter in self.filters:
            infos['filters'][component_filter.name] = component_filter.to_database()
        return infos

    @classmethod
    def from_database(cls, slot_name: str, slot_infos: dict[str, Any]):
        multiple = slot_infos['multiple']

        # get filters
        filters: list[ComponentFilterBase] = []
        for filter_name, filter_infos in slot_infos['filters'].items():
            filters.append(ComponentFilters.from_name(name=filter_name).from_database(infos=filter_infos))

        ingredient_slot = cls(name=slot_name, multiple=multiple, filters=filters)
        return ingredient_slot


class Ingredients:
    def __init__(self, name: str, versions: list[Version]):
        """
        List of the ingredients of a recipe, grouped by their name.
        :param name: name of the ingredient
        :param versions: versions imported under this name
        """
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
