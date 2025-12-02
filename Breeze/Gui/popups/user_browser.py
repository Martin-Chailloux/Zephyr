from PySide6.QtWidgets import QVBoxLayout

from Api.breeze_app import BreezeApp
from Api.document_models.studio_documents import User
from Gui.mvd.user_mvd.user_list_view import UserListView
from Gui.popups.abstract_popup_widget import AbstractPopupWidget


class UserBrowser(AbstractPopupWidget):
    project = BreezeApp.project
    users = project.users

    def __init__(self, default_user: User = None):
        super().__init__(w=168, h=248)
        self.default_user = default_user
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        users_list = UserListView()
        layout.addWidget(users_list)
        if self.default_user is not None:
            users_list.set_selected_user(self.default_user)

        self.users_list = users_list

    def _connect_signals(self):
        self.users_list.right_clicked.connect(self.reject)
        self.users_list.selectionModel().selectionChanged.connect(self.accept)
