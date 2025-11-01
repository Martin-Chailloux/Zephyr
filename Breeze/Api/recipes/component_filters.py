from dataclasses import dataclass
from typing import Any, Type

from Api.document_models.project_documents import Component


class ComponentFilterBase:
    name: str

    def __init__(self, items: list[str], is_reversed: bool=False):
        """
        :param items: list of items to include
        :param is_reversed: if True, parm items becomes a list of items to avoid
        """
        self.items = [s.lower() for s in items]
        self.is_reversed = is_reversed

    def get_filtered_components(self, components: list[Component]) -> list[Component]:
        input_components = components
        components = [c for c in components if c.stage.asset.category.lower() in self.items]
        components = self.filter_components(components=components)
        if self.is_reversed:
            components = [c for c in input_components if c not in components]
        return components

    def filter_components(self, components: list[Component]) -> list[Component]:
        return components

    def to_database(self) -> dict[str, Any]:
        result = {'items': self.items, 'is_reversed': self.is_reversed}
        return result

    @classmethod
    def from_database(cls, infos: dict[str, Any]):
        items = infos['items']
        is_reversed = infos['is_reversed']
        return cls(items=items, is_reversed=is_reversed)


class ComponentFilterCategory(ComponentFilterBase):
    name = 'category'
    def filter_components(self, components: list[Component]) -> list[Component]:
        components = [c for c in components if c.stage.asset.category.lower() in self.items]
        return components


class ComponentFilterStage(ComponentFilterBase):
    name = 'stage'
    def get_filtered_components(self, components: list[Component]) -> list[Component]:
        components = [c for c in components if c.stage.stage_template.name in self.items]
        return components


class ComponentFilterComponent(ComponentFilterBase):
    name = 'component'
    def get_filtered_components(self, components: list[Component]) -> list[Component]:
        components = [c for c in components if c.name in self.items]
        return components


@dataclass
class ComponentFilters:
    Category = ComponentFilterCategory
    Stage = ComponentFilterStage
    Component = ComponentFilterComponent

    @classmethod
    def from_name(cls, name: str) -> Type[ComponentFilterBase]:
        for component_filter in [cls.Category, cls.Stage, cls.Component]:
            if name == component_filter.name:
                return component_filter
        else:
            raise ValueError(f"Did not find a ComponentFilter with name {name}")
