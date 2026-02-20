from typing import Optional

from PySide6.QtCore import Signal, QItemSelectionModel

from Api.document_models.project_documents import SubUser
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

    def set_users(self, users: list[User]):
        if users is None:
            users = []
        self._model.populate(users=users)

    def set_all_users(self):
        self._model.populate(users=User.objects())

    def set_sub_users(self):
        users = [sub_user.source_user for sub_user in SubUser.objects()]
        self.set_users(users=users)

    def set_available_users(self):
        working_users = [sub_user.source_user for sub_user in SubUser.objects()]
        available_users = [user for user in User.objects if user not in working_users]
        self.set_users(users=available_users)

    def set_selected_user(self, user: User):
        indexes = [self._model.index(row, 0) for row in range(self._model.rowCount())]
        for index in indexes:
            if index.data(UserItemRoles.user) == user:
                self.selectionModel().setCurrentIndex(index, QItemSelectionModel.SelectionFlag.Select)
                return

    def get_user(self) -> Optional[User]:
        index = self.get_selected_index()
        if index is None:
            return None
        user: User = index.data(UserItemRoles.user)
        return user

    def get_sub_user(self) -> Optional[SubUser]:
        user = self.get_user()
        if user is None:
            return user
        sub_user = SubUser.from_pseudo(pseudo=user.pseudo)
        return sub_user