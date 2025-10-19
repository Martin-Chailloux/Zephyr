from typing import Optional

from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QFrame, QSizePolicy

from Api.document_models.project_documents import Stage
from Gui.mvd.component_mvd.component_tree_view import ComponentTreeView
from Utils.sub_widgets import IconButton


class IngredientsSubPanel(QWidget):
    def __init__(self, stage: Optional[Stage]):
        super().__init__()
        self.stage = stage
        self._init_ui()
        self._connect_signals()
        self._init_state()

    def set_stage(self, stage: Stage = None):
        self.stage = stage
        self.ingredients_view.set_stage(stage=stage)
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

        ingredients_view = ComponentTreeView()
        sub_layout.addWidget(ingredients_view)
        ingredients_view.set_stage(stage=self.stage)

        self.toolbar = toolbar
        self.ingredients_view = ingredients_view

    def _connect_signals(self):
        self.ingredients_view.selectionModel().selectionChanged.connect(self.on_ingredient_selection_changed)

    def _init_state(self):
        self.on_ingredient_selection_changed()

    def on_ingredient_selection_changed(self):
        selected_indexes = self.ingredients_view.selectionModel().selectedIndexes()

        for button in [self.toolbar.group_button, self.toolbar.copy_button,
                       self.toolbar.paste_button, self.toolbar.delete_button]:
            button.setEnabled(len(selected_indexes) > 0)

class ToolBar(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._init_ui()

    def _init_ui(self):
        pass

    def add_divider(self) -> QFrame:
        # TODO: the stylesheet removes the line
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Plain)
        divider.setFixedHeight(12)
        self.layout().addWidget(divider)
        return divider

    def add_button(self, icon_name: str, tooltip: str) -> QPushButton:
        button = IconButton(icon_name=icon_name, wh=28, icon_size=24)
        button.setToolTip(tooltip)
        self.layout().addWidget(button)
        return button


class IngredientsToolBar(ToolBar):
    def _init_ui(self):
        self.refresh_button = self.add_button(icon_name='fa.refresh', tooltip='Refresh')
        self.autofill_button = self.add_button(icon_name='fa5s.check-circle', tooltip='Autofill')
        self.add_divider()
        self.group_button = self.add_button(icon_name='fa5s.folder-plus', tooltip='Create group')
        self.copy_button = self.add_button(icon_name='fa5s.copy', tooltip='Copy')
        self.paste_button = self.add_button(icon_name='fa.paste', tooltip='Paste')
        self.add_divider()
        self.delete_button = self.add_button(icon_name='fa5s.trash', tooltip='Delete')
