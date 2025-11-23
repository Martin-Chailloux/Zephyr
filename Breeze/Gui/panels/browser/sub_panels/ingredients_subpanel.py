from typing import Optional

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout

from Api.document_models.project_documents import Stage
from Api.recipes.ingredient_slot import IngredientSlot
from Gui.mvd.component_mvd.component_tree_model import ComponentTreeItemRoles
from Gui.mvd.component_mvd.component_tree_view import ComponentTreeView
from Gui.sub_widgets.toolbar import ToolBar


class IngredientsSubPanel(QWidget):
    def __init__(self, stage: Optional[Stage]):
        super().__init__()
        self.stage = stage
        self._init_ui()
        self._connect_signals()
        self._init_state()

    def set_stage(self, stage: Stage = None):
        self.stage = stage
        self.ingredients_list.set_stage(stage=stage)
        self._init_state()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("Ingredients")
        layout.addWidget(title)

        sub_layout = QHBoxLayout()
        layout.addLayout(sub_layout)

        toolbar = IngredientsToolBar()
        sub_layout.addWidget(toolbar)

        ingredients_list = ComponentTreeView()
        sub_layout.addWidget(ingredients_list)
        ingredients_list.set_stage(stage=self.stage)

        self.toolbar = toolbar
        self.ingredients_list = ingredients_list

    def refresh(self):
        self.ingredients_list.refresh()

    def _connect_signals(self):
        self.ingredients_list.selectionModel().selectionChanged.connect(self.on_selection_changed)
        self.toolbar.delete_button.clicked.connect(self.delete_selected_items)

    def _init_state(self):
        self.on_selection_changed()

    def on_selection_changed(self):
        selected_indexes = self.ingredients_list.selectedIndexes()

        for button in [self.toolbar.group_button, self.toolbar.copy_button,
                       self.toolbar.paste_button, self.toolbar.delete_button]:
            button.setEnabled(len(selected_indexes) > 0)

    def delete_selected_items(self):
        # sort selection by names
        to_delete = {}
        for index in self.ingredients_list.selectedIndexes():
            if index.data(ComponentTreeItemRoles.is_title):
                continue

            ingredient_slot: IngredientSlot = index.data(ComponentTreeItemRoles.ingredient_slot)
            name = ingredient_slot.name
            if name not in to_delete:
                to_delete[name] = []
            to_delete[name].append(index.data(ComponentTreeItemRoles.version))

        # update the stage's ingredients
        for name, deleted_versions in to_delete.items():
            versions = self.stage.ingredients[name]
            for deleted_version in deleted_versions:
                versions.remove(deleted_version)  # remove 1 by 1 in case the same version is called twice
            self.stage.ingredients[name] = versions
        self.stage.save()


        # refresh the model
        self.ingredients_list.refresh()


class IngredientsToolBar(ToolBar):
    def _init_ui(self):
        self.refresh_button = self.add_button(icon_name='fa.refresh', tooltip='Refresh')
        self.autofill_button = self.add_button(icon_name='fa5s.sign-in-alt', tooltip='Autofill')
        self.add_divider()
        self.group_button = self.add_button(icon_name='fa5s.folder-plus', tooltip='Create group')
        self.copy_button = self.add_button(icon_name='fa5s.copy', tooltip='Copy')
        self.paste_button = self.add_button(icon_name='fa.paste', tooltip='Paste')
        self.add_divider()
        self.delete_button = self.add_button(icon_name='fa5s.trash', tooltip='Delete')
