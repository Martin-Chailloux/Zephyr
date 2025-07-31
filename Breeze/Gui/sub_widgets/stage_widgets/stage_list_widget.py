from typing import Optional

import qtawesome

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QSizePolicy)

from Api.project_documents import Asset
from Gui.components.popups.set_stage_templates_popup import SetStageTemplatesPopup
from Gui.sub_widgets.stage_templates_widgets.stage_item import StageItem
from Gui.components.mvd.stage_mvd.stage_list_view import StageListEditableView


class StageListWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.asset: Optional[Asset] = None
        self.stage_items: list[StageItem] = []
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(0, 7, 0, 0)
        layout.setSpacing(5)

        stage_list = StageListEditableView()
        layout.addWidget(stage_list)

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
        self.stage_list = stage_list

    def set_asset(self, asset: Asset = None):
        self.asset = asset
        self.stage_list.set_asset(asset)

    # ------------------------
    # Events
    # ------------------------
    def on_edit_stages_clicked(self):
        selected_stage = self.stage_list.stage

        popup = SetStageTemplatesPopup(asset=self.asset)
        popup.exec()
        self.stage_list.set_asset(self.asset)

        if selected_stage is not None:
            self.stage_list.select_stage(stage=selected_stage)
