from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtGui import QStandardItem, QStandardItemModel

from Api.project_documents import Component, Version


@dataclass
class VersionItemRoles:
    version = QtCore.Qt.ItemDataRole.UserRole

@dataclass
class VersionItemMetrics:
    height: int = 36


class VersionListModel(QStandardItemModel):
    def __init__(self):
        super().__init__()
        self.versions: list[Version] = []

    def add_item(self, version: Version):
        row = self.rowCount()

        item = QStandardItem()
        item.setSizeHint(QSize(0, VersionItemMetrics.height))
        item.setEditable(False)

        item.setData(version, VersionItemRoles.version)

        self.setItem(row, item)

    def populate(self, versions: list[Version]):
        self.versions = versions

        self.clear()

        versions = sorted(versions, key=lambda v: v.number, reverse=True)
        for version in versions:
            self.add_item(version=version)

    def refresh(self):
        if not self.versions:
            return

        self.blockSignals(True)
        component = self.versions[0].component
        # longnames = [version.longname for version in component.versions]
        # versions = Version.objects(longname__in=longnames)
        self.populate(component.versions)
        self.blockSignals(False)
