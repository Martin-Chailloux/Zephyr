from PySide6 import QtCore
from PySide6.QtCore import Signal, QItemSelectionModel
from PySide6.QtGui import QMouseEvent

from Data.studio_documents import User
from Gui.abstract_widgets.abstract_mvd import AbstractListView
from Gui.user_widgets.user_list.user_list_item_delegate import UserListItemDelegate
from Gui.user_widgets.user_list.user_list_model import UserListModel, UserItemRoles


class UserListView(AbstractListView):
    user_selected = Signal(str)
    right_clicked = Signal()

    def __init__(self):
        super().__init__()
        self._model = UserListModel()
        self.setModel(self._model)

        self._item_delegate = UserListItemDelegate()
        self.setItemDelegate(self._item_delegate)

    def set_selected_user(self, user: User):
        indexes = [self._model.index(row, 0) for row in range(self._model.rowCount())]
        for index in indexes:
            if index.data(UserItemRoles.user) == user:
                self.selectionModel().setCurrentIndex(index, QItemSelectionModel.SelectionFlag.Select)
                return

    def mousePressEvent(self, event):
        if isinstance(event, QMouseEvent):
            if event.button() == QtCore.Qt.MouseButton.RightButton:
                self.right_clicked.emit()
                return

        super().mousePressEvent(event)
        user = self._get_hovered_item().data(UserItemRoles.user)
        self.user_selected.emit(user.pseudo)

    # def mouseDoubleClickEvent(self, event):
    #     super().mouseDoubleClickEvent(event)
    #     user = self._get_hovered_item().data(UserItemRoles.user)
    #     self.user_selected.emit(user.pseudo)
