from typing import Optional

import qtawesome
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from Api.project_documents import Stage
from Gui.mvd.component_mvd.component_tree_view import ComponentTreeView
from Api.recipes.ingredients import IngredientSlot
from Api.recipes.component_filters import ComponentFilters


class IngredientTreeWidget(QWidget):
    def __init__(self, stage: Optional[Stage]):
        super().__init__()
        self.stage = stage
        self._init_ui()

    def set_stage(self, stage: Stage = None):
        self.stage = stage
        self.ingredients_view.set_stage(stage=stage)

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        ingredients_view = ComponentTreeView()
        layout.addWidget(ingredients_view)
        ingredients_view.set_stage(stage=self.stage)

        # TODO: an empty item that serves as a searchbar, when entered it brings the component's popup where one can be selected and added
        #  same ui for the recipe, with a filter that only shows the components that matches the recipe

        # TODO: double click a component to edit its infos ?

        add_ingredient_button = QPushButton("Add")
        layout.addWidget(add_ingredient_button)
        add_ingredient_button.setIcon(qtawesome.icon('fa.plus-circle'))

        add_ingredient_button.clicked.connect(self.on_add_clicked)

        self.ingredients_view = ingredients_view

    def on_add_clicked(self):
        return
        # Ingredient(recipe=None, stage_in=['modeling'], component_in=['geo'])
        IngredientSlot(recipe=None, filters=[
            ComponentFilters.stage(items=['modeling'], exclude=True),
        ])