from dataclasses import dataclass
from typing import Optional

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtGui import QStandardItem
from PySide6.QtWidgets import QCheckBox, QComboBox

from Api.project_documents import Component, Stage, Version
from Api.recipes import Ingredients, Recipe, IngredientSlot
from Api.studio_documents import StageTemplate
from Gui.components.mvd.abstract_mvd import AbstractItemModel


@dataclass
class ComponentTreeItemRoles:
    is_title = QtCore.Qt.ItemDataRole.UserRole
    label = QtCore.Qt.ItemDataRole.UserRole + 1
    version = QtCore.Qt.ItemDataRole.UserRole + 2
    ingredient_slot = QtCore.Qt.ItemDataRole.UserRole + 3


@dataclass
class ComponentTreeItemMetrics:
    height: int = 28


class ComponentTreeModel(AbstractItemModel):
    def __init__(self):
        super().__init__()
        self.stage: Optional[Stage] = None
        self.ingredients = []
        # self.components: list[Component] = []
        #
        # top_item_recipe = self.add_top_item(label="Recipe")
        # top_item_extra = self.add_top_item(label="Extra")
        #
        #
        # # [DEV] all components for now
        # components: list[Component] = Component.objects
        # stage_templates: dict[StageTemplate, list[Component]] = {}
        #
        # # sort by stage template
        # for component in components:
        #     stage_template = component.stage.stage_template
        #     if stage_template not in stage_templates.keys():
        #         stage_templates[stage_template] = []
        #     stage_templates[stage_template].append(component)
        #
        # # add items
        # self.add_create_item(parent=top_item_extra)
        # for stage_template, components in stage_templates.items():
        #     stage_template_item = self.add_stage_template_item(parent=top_item_extra, stage_template=stage_template)
        #     components = sorted(components, key=lambda c: c.longname)
        #     for component in components:
        #         self.add_component_item(parent=stage_template_item, component=component)

    def populate(self, stage: Stage = None):
        print("POPULATE")
        self.stage = stage

        self.clear()
        self.ingredients = []
        # self.setColumnCount(1)
        # self.setHorizontalHeaderLabels(['Name'])

        if stage is None:
            return

        for name, versions in self.stage.ingredients.items():
            self.ingredients.append(Ingredients(name=name, versions=versions))

        # add top items
        recipe = Recipe.from_database(recipe_infos=stage.stage_template.recipe)
        for ingredient_slot in recipe.ingredients_slots:
            self.add_top_item(ingredient_slot=ingredient_slot)
        # self.add_top_item(ingredient_slot=IngredientSlot(name="Extra"))  # Permanent extra slot

        # for ingredient_infos in stage.recipe_ingredients:
        #     ingredient = Ingredient.from_database(ingredient_infos=ingredient_infos)

    def add_top_item(self, ingredient_slot: IngredientSlot) -> QStandardItem:
        item = QStandardItem()
        item.setData(True, ComponentTreeItemRoles.is_title)
        item.setSizeHint(QSize(0, ComponentTreeItemMetrics.height + 8))

        label = ingredient_slot.name.title()
        item.setData(label, ComponentTreeItemRoles.label)
        item.setSelectable(False)
        item.setEditable(False)

        self.appendRow(item)

        has_ingredients: bool = False
        for ingredient in self.ingredients:
            if ingredient.name == ingredient_slot.name:
                for version in ingredient.versions:
                    self.add_sub_item(parent=item, ingredient_slot=ingredient_slot, version=version)
                has_ingredients = True

        if ingredient_slot.is_multiple or not has_ingredients:
            self.add_sub_item(parent=item, ingredient_slot=ingredient_slot, version=None)

        return item

    def add_sub_item(self, parent: QStandardItem, ingredient_slot: IngredientSlot, version: Version=None) -> QStandardItem:
        item = QStandardItem()
        item.setSizeHint(QSize(0, ComponentTreeItemMetrics.height))
        item.setData(False, ComponentTreeItemRoles.is_title)
        item.setData(version, ComponentTreeItemRoles.version)
        item.setData(ingredient_slot, ComponentTreeItemRoles.ingredient_slot)

        item.setSelectable(version is not None)

        row = parent.rowCount()
        parent.setChild(row, item)
        return item
