from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtGui import QStandardItem

from Data.project_documents import Asset, Stage
from Gui.abstract_widgets.abstract_mvd import AbstractListModel


@dataclass
class StageItemRoles:
    stage = QtCore.Qt.ItemDataRole.UserRole
    user_is_hovered = QtCore.Qt.ItemDataRole.UserRole + 1
    status_is_hovered = QtCore.Qt.ItemDataRole.UserRole + 2


@dataclass
class StageItemMetrics:
    height: int = 36
    logo_w: int = 48
    status_w: int = 52


class StageListModel(AbstractListModel):
    def __init__(self):
        super().__init__()
        self.asset: Asset = None

    def set_asset(self, asset: Asset):
        self.asset = asset
        if asset is None:
            return

        self.clear()
        for stage in asset.stages:
            self.add_item(stage=stage)

    def add_item(self, stage: Stage):
        row = self.rowCount()

        item = QStandardItem()
        item.setSizeHint(QSize(0, StageItemMetrics.height))
        item.setEditable(False)

        item.setData(stage, StageItemRoles.stage)
        item.setData(False, StageItemRoles.user_is_hovered)
        item.setData(False, StageItemRoles.status_is_hovered)

        self.setItem(row, item)

    def refresh(self):
        stages = [item.data(StageItemRoles.stage) for item in self.items]
        if len(stages) <= 1:
            return
        stages = Asset.objects.get(longname=stages[0].asset.longname).stages  # query the data from db else it is not up to date

        self.blockSignals(True)
        self.clear()
        for stage in stages:
            self.add_item(stage=stage)
        self.blockSignals(False)

    def remove_items_hover(self):
        for item in self.items:
            item.setData(False, StageItemRoles.user_is_hovered)
            item.setData(False, StageItemRoles.status_is_hovered)
