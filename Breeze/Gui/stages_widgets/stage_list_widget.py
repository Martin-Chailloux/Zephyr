import qtawesome

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QSizePolicy)

from Data.project_documents import StageTemplate, Asset, Stage
from Dialogs.breeze_dialog import create_stage
from Gui.stage_templates_widgets.select_stage_templates import StageTemplateSelector
from Gui.stages_widgets.stage_item import StageItem
from Gui.stages_widgets.stages_list.stages_list_view import StageListView


class StageListWidget(QWidget):
    margin: int = 7

    def __init__(self, asset: Asset):
        super().__init__()
        self.current_asset: Asset = asset
        self.stage_items: list[StageItem] = []
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(self.margin, self.margin, self.margin, self.margin)
        layout.setSpacing(5)

        stages_list_view = StageListView()
        layout.addWidget(stages_list_view)

        # 'Edit' button
        edit_button = QPushButton(" Edit stages")
        layout.addWidget(edit_button)
        edit_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        edit_button.setIcon(qtawesome.icon("mdi.format-list-checkbox"))
        edit_button.setIconSize(QSize(22, 22))
        edit_button.clicked.connect(self.on_edit_stages_clicked)

        edit_button.setFixedHeight(26)

        # public vars
        self.new_button = edit_button
        self.stage_list_view = stages_list_view

    def set_current_asset(self, asset: Asset):
        self.current_asset = asset
        self.refresh()

    def refresh(self):
        self.stage_list_view.set_asset(self.current_asset)

    # ------------------------
    # Events
    # ------------------------
    def on_edit_stages_clicked(self):
        popup = StageTemplateSelector(asset=self.current_asset)
        popup.exec()
        self.refresh()
