from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtCore import QSize, QSortFilterProxyModel
from PySide6.QtGui import QStandardItem

from Api.document_models.project_documents import Version
from Gui.mvd.abstract_mvd import AbstractItemModel


@dataclass
class VersionItemRoles:
    version = QtCore.Qt.ItemDataRole.UserRole

@dataclass
class VersionItemMetrics:
    height: int = 36


class VersionListModel(AbstractItemModel):
    def __init__(self):
        super().__init__()
        self.proxy = QSortFilterProxyModel()
        self.proxy.setSourceModel(self)

        self.versions: list[Version] = []

    def add_item(self, version: Version):
        row = self.rowCount()

        item = QStandardItem()
        item.setSizeHint(QSize(0, VersionItemMetrics.height))
        item.setEditable(False)

        item.setData(version, VersionItemRoles.version)
        item.setData(version.get_filter_keys(), QtCore.Qt.ItemDataRole.DisplayRole)  # used for filtering

        self.setItem(row, item)

    def set_text_filter(self, text: str):
        text = text.replace(' ', '*')
        self.proxy.setFilterWildcard(text)

    def populate(self, versions: list[Version]):
        self.versions = versions

        self.clear()

        versions = sorted(versions, key=lambda v: v.number, reverse=True)
        for version in versions:
            self.add_item(version=version)

    def refresh(self):
        if not self.versions:
            print(f"WARNING: VersionListModel has no version, cant fetch new versions based on component")
            return

        self.blockSignals(True)
        component = self.versions[0].component
        self.populate(versions=component.versions)
        self.blockSignals(False)
