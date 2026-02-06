from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtGui import QStandardItem

from Api.breeze_app import BreezeApp
from Api.document_models.project_documents import SubUser
from Api.document_models.studio_documents import User
from Gui.mvd.abstract_mvd import AbstractItemModel


@dataclass
class UserItemRoles:
    user = QtCore.Qt.ItemDataRole.UserRole

@dataclass
class UserItemMetrics:
    height: int = 32


class UserListModel(AbstractItemModel):
    def __init__(self):
        super().__init__()
        self.populate()

    def add_item(self, user: User):
        row = self.rowCount()

        item = QStandardItem()
        item.setSizeHint(QSize(0, UserItemMetrics.height))
        item.setEditable(False)

        item.setData(user, UserItemRoles.user)

        self.setItem(row, item)

    def populate(self):
        self.clear()
        for user in SubUser.objects():
            self.add_item(user)
