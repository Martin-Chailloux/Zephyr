from PySide6.QtCore import Signal, QItemSelectionModel

from Api.document_models.studio_documents import User
from Gui.mvd.abstract_mvd import AbstractListView
from Gui.mvd.user_mvd.user_list_item_delegate import UserListItemDelegate
from Gui.mvd.user_mvd.user_list_model import UserListModel, UserItemRoles


class UserListView(AbstractListView):
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

    def get_user(self) -> User:
        index = self.get_selected_index()
        user: User = index.data(UserItemRoles.user)
        return user
