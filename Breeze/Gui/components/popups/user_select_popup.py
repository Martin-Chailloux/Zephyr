from PySide6.QtWidgets import QVBoxLayout

from Api.breeze_app import BreezeApp
from Api.project_documents import Stage
from Api.studio_documents import User
from Gui.components.mvd.user_mvd.user_list_view import UserListView
from Gui.components.popups.abstract_popup_widget import AbstractPopupWidget


class UserSelectPopup(AbstractPopupWidget):
    project = BreezeApp.project
    users = project.users

    def __init__(self, stage: Stage):
        super().__init__(w=168, h=248, position=[0.5, 0.25])
        self.stage = stage
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        users_list = UserListView()
        layout.addWidget(users_list)
        users_list.set_selected_user(self.stage.user)

        self.users_list = users_list

    def _connect_signals(self):
        self.users_list.user_selected.connect(self.on_user_selected)
        self.users_list.right_clicked.connect(self.reject)

    def on_user_selected(self, pseudo: str):
        user = User.objects.get(pseudo=pseudo)
        self.stage.update(user=user)
        self.accept()
