from dataclasses import dataclass
from typing import Any

from Api.project_documents import Component


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
        components = [c for c in components if c.stage.stage_template.label.lower() in self.items]
        return components


@dataclass
class ComponentFilters:
    category = ComponentFilterCategory
    stage = ComponentFilterStage

    @classmethod
    def from_name(cls, name: str) -> ComponentFilterBase.__class__:
        for component_filter in [cls.category, cls.stage]:
            if name == component_filter.name:
                return component_filter
        else:
            raise ValueError(f"Did not find a ComponentFilter with name {name}")
