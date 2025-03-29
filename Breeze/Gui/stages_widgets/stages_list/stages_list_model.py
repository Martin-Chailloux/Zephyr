from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtGui import QStandardItemModel, QStandardItem

from Data.breeze_documents import Asset, Stage


@dataclass
class StageItemRoles:
    stage = QtCore.Qt.ItemDataRole.UserRole


@dataclass
class StageListItemSizes:
    height: int = 36
    logo_w: int = 48
    status_w: int = 48


class StageListModel(QStandardItemModel):
    def __init__(self):
        super().__init__()

    def set_asset(self, asset: Asset):
        self.clear()
        for stage in asset.stages:
            self.add_item(stage=stage)


    def add_item(self, stage: Stage):
        row = self.rowCount()

        item = QStandardItem()
        item.setSizeHint(QSize(0, StageListItemSizes.height))
        item.setEditable(False)

        item.setData(stage, StageItemRoles.stage)
        self.setItem(row, item)