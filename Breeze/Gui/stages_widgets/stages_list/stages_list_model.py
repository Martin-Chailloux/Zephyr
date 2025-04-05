from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtGui import QStandardItemModel, QStandardItem

from Data.breeze_documents import Asset, Stage


@dataclass
class StageItemRoles:
    stage = QtCore.Qt.ItemDataRole.UserRole
    user_is_hovered = QtCore.Qt.ItemDataRole.UserRole + 1
    status_is_hovered = QtCore.Qt.ItemDataRole.UserRole + 2


@dataclass
class StageListItemSizes:
    height: int = 36
    logo_w: int = 48
    status_w: int = 52


class StageListModel(QStandardItemModel):
    def __init__(self):
        super().__init__()
        self.asset: Asset = None

    def set_asset(self, asset: Asset):
        self.asset = asset
        self.clear()
        if asset is not None:
            for stage in asset.stages:
                self.add_item(stage=stage)

    def add_item(self, stage: Stage):
        row = self.rowCount()

        item = QStandardItem()
        item.setSizeHint(QSize(0, StageListItemSizes.height))
        item.setEditable(False)

        item.setData(stage, StageItemRoles.stage)
        item.setData(False, StageItemRoles.user_is_hovered)
        item.setData(False, StageItemRoles.status_is_hovered)
        self.setItem(row, item)

    @property
    def items(self):
        items = [self.item(row) for row in range(self.rowCount())]
        return items

    def remove_items_hover(self):
        for item in self.items:
            item.setData(False, StageItemRoles.user_is_hovered)
            item.setData(False, StageItemRoles.status_is_hovered)
