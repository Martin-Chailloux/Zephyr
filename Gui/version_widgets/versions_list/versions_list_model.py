from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtCore import QAbstractItemModel, QModelIndex, QSize
from PySide6.QtGui import QStandardItemModel, QStandardItem


@dataclass
class VersionItemRoles:
    name = QtCore.Qt.ItemDataRole.UserRole
    number = QtCore.Qt.ItemDataRole.UserRole + 1
    # TODO:
    #   - hour
    #   - date


class VersionsListModel(QStandardItemModel):
    def __init__(self):
        super().__init__()

    def add_item(self, version):
        row_count = self.rowCount()

        item = QStandardItem()
        item.setSizeHint(QSize(0, 30))
        item.setEditable(False)

        item.setData("im a version yay", VersionItemRoles.name)
        item.setData(version, VersionItemRoles.number)

        self.setItem(row_count, item)
