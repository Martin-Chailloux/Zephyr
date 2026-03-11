from PySide6.QtWidgets import QVBoxLayout

from Breeze.Api.breeze_app import BreezeApp
from Breeze.Api.document_models.studio_documents import User
from Breeze.Gui.mvd.user_mvd.user_list_view import UserListView
from Breeze.Gui.popups.abstract_popup_widget import AbstractPopupWidget


class UserBrowser(AbstractPopupWidget):
    project = BreezeApp.project
    users = project.users

    def __init__(self, default_user: User = None, from_sub_users: bool=True):
        super().__init__(w=168, h=248)
        self.default_user = default_user
        self.from_sub_users = from_sub_users

        self._init_ui()
        self._connect_signals()
        self._init_state()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        users_list = UserListView()
        layout.addWidget(users_list)

        self.users_list = users_list

    def _connect_signals(self):
        self.users_list.right_clicked.connect(self.reject)
        self.users_list.selectionModel().selectionChanged.connect(self.accept)

    def _init_state(self):
        if self.from_sub_users:
            self.users_list.set_sub_users()
        else:
            self.users_list.set_users()

        if self.default_user is not None:
            self.users_list.set_selected_user(self.default_user)
