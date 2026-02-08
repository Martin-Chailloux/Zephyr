from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtGui import QStandardItem

from Api.document_models.project_documents import Asset
from Gui.mvd.abstract_mvd import AbstractItemModel


@dataclass
class AssetItemRoles:
    asset = QtCore.Qt.ItemDataRole.UserRole
    can_bookmark = QtCore.Qt.ItemDataRole.UserRole + 1


@dataclass
class AssetItemMetrics:
    height: int = 36


class AssetListModel(AbstractItemModel):
    item_h = AssetItemMetrics.height

    def __init__(self):
        super().__init__()
        self.assets = []

    def populate(self, assets: list[Asset]):
        self.assets = assets

        self.clear()

        for asset in assets:
            self.add_item(asset=asset)

    def refresh(self):
        self.blockSignals(True)

        assets = []
        for asset in self.assets:
            asset.reload()
            assets.append(asset)

        self.populate(assets)
        self.blockSignals(False)

    def add_item(self, asset: Asset):
        row = self.rowCount()

        item = QStandardItem()
        item.setSizeHint(QSize(0, self.item_h))
        item.setEditable(False)

        item.setData(asset, AssetItemRoles.asset)
        item.setData(False, AssetItemRoles.can_bookmark)

        self.setItem(row, item)

    def clear_hover_data(self):
        for item in self.items:
            item.setData(False, AssetItemRoles.can_bookmark)
