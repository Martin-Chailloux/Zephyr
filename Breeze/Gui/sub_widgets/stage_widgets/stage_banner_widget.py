from typing import Optional

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QSizePolicy

from Api.document_models.project_documents import Stage
from Gui.mvd.stage_mvd.stage_list_item_delegate import StageListItemDelegateHighlighted
from Gui.mvd.stage_mvd.stage_list_model import StageItemMetrics
from Gui.mvd.stage_mvd.stage_list_view import StageListViewEditable


class StageBannerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self.stage: Optional[Stage] = None

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)

        # show asset
        asset_label = QLabel()
        layout.addWidget(asset_label)
        asset_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # show stage
        stage_list = StageListViewEditable()
        layout.addWidget(stage_list)
        stage_list.setMaximumSize(QSize(256, StageItemMetrics.height + 6))
        stage_list.setItemDelegate(StageListItemDelegateHighlighted())

        # public vars
        self._asset_label = asset_label
        self.stage_list = stage_list

    def set_stage(self, stage: Stage = None):
        self.stage = stage

        # asset
        if stage is not None:
            text = f"{stage.asset.category} ⮞ {stage.asset.name} ⮞ {stage.asset.variant}"
            self._asset_label.setText(text)

        # stage
        self.stage_list.set_stage(stage)

