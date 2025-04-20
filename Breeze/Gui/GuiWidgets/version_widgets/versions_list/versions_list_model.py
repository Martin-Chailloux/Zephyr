from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtGui import QStandardItem, QStandardItemModel

from Data.project_documents import Collection, Version


@dataclass
class VersionItemRoles:
    version = QtCore.Qt.ItemDataRole.UserRole

@dataclass
class VersionItemMetrics:
    height: int = 32


class VersionListModel(QStandardItemModel):
    def __init__(self, collection: Collection):
        super().__init__()
        self.collection = collection
        self.populate()

    def add_item(self, version: Version):
        row = self.rowCount()

        item = QStandardItem()
        item.setSizeHint(QSize(0, VersionItemMetrics.height))
        item.setEditable(False)

        item.setData(version, VersionItemRoles.version)

        self.setItem(row, item)

    def populate(self):
        self.clear()
        if self.collection is None:
            return

        versions: list[Version] = self.collection.versions
        versions = sorted(versions, key=lambda v: v.number, reverse=True)
        for version in versions:
            self.add_item(version=version)
