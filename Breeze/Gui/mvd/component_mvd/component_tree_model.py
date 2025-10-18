from dataclasses import dataclass
from typing import Optional

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtGui import QStandardItem

from Api.document_models.project_documents import Stage, Version
from Api.recipes.recipe import Recipe
from Api.recipes.ingredients import Ingredients
from Api.recipes.ingredients import IngredientSlot
from Gui.mvd.abstract_mvd import AbstractItemModel


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

    def populate(self, stage: Stage = None):
        self.stage = stage

        self.clear()
        self.ingredients = []

        if stage is None:
            return

        for name, versions in self.stage.ingredients.items():
            self.ingredients.append(Ingredients(name=name, versions=versions))

        # add top items
        recipe = Recipe.from_database(infos=stage.stage_template.recipe)
        for ingredient_slot in recipe.ingredients_slots:
            self.add_top_item(ingredient_slot=ingredient_slot)

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
