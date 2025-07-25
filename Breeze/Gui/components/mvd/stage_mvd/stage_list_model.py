from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtGui import QStandardItem

from Api.project_documents import Stage
from Gui.components.mvd.abstract_mvd import AbstractListModel


@dataclass
class StageItemRoles:
    stage = QtCore.Qt.ItemDataRole.UserRole
    user_is_hovered = QtCore.Qt.ItemDataRole.UserRole + 1
    status_is_hovered = QtCore.Qt.ItemDataRole.UserRole + 2


@dataclass
class StageItemMetrics:
    height: int = 42
    height_minimal: int = 36
    logo_w: int = 48
    status_w: int = 52


class StageListModel(AbstractListModel):
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
        longnames = [stage.longname for stage in self.stages]
        stages = Stage.objects(longname__in=longnames)
        self.populate(stages)
        self.blockSignals(False)

    def add_item(self, stage: Stage):
        row = self.rowCount()

        item = QStandardItem()
        item.setSizeHint(QSize(0, self.item_h))
        item.setEditable(False)

        item.setData(stage, StageItemRoles.stage)
        item.setData(False, StageItemRoles.user_is_hovered)
        item.setData(False, StageItemRoles.status_is_hovered)

        self.setItem(row, item)

    def remove_items_hover(self):
        for item in self.items:
            item.setData(False, StageItemRoles.user_is_hovered)
            item.setData(False, StageItemRoles.status_is_hovered)

class StageListMinimalModel(StageListModel):
    item_h = StageItemMetrics.height_minimal
