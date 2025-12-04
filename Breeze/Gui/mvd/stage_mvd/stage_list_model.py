from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtGui import QStandardItem

from Api.document_models.project_documents import Stage
from Gui.mvd.abstract_mvd import AbstractItemModel


@dataclass
class StageItemRoles:
    stage = QtCore.Qt.ItemDataRole.UserRole
    can_edit_user = QtCore.Qt.ItemDataRole.UserRole + 1
    can_edit_status = QtCore.Qt.ItemDataRole.UserRole + 2


@dataclass
class StageItemMetrics:
    height: int = 42
    height_minimal: int = 36
    logo_width: int = 48
    status_width: int = 52


class StageListModel(AbstractItemModel):
    item_h = StageItemMetrics.height

    def __init__(self):
        super().__init__()
        self.stages = []

    def populate(self, stages: list[Stage]):
        self.stages = stages

        self.clear()
        stages = sorted(stages, key=lambda x: x.stage_template.order)

        for stage in stages:
            self.add_item(stage=stage)

    def refresh(self):
        self.blockSignals(True)

        stages = []
        for stage in self.stages:
            stage.reload()
            stages.append(stage)

        self.populate(stages)
        self.blockSignals(False)

    def add_item(self, stage: Stage):
        row = self.rowCount()

        item = QStandardItem()
        item.setSizeHint(QSize(0, self.item_h))
        item.setEditable(True)

        item.setData(stage, StageItemRoles.stage)
        item.setData(False, StageItemRoles.can_edit_user)
        item.setData(False, StageItemRoles.can_edit_status)

        self.setItem(row, item)

    def clear_hover_data(self):
        for item in self.items:
            item.setData(False, StageItemRoles.can_edit_user)
            item.setData(False, StageItemRoles.can_edit_status)


class StageListMinimalModel(StageListModel):
    item_h = StageItemMetrics.height_minimal
