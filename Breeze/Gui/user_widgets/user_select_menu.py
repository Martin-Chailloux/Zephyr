from PySide6.QtWidgets import QVBoxLayout, QApplication

from Data import app_dialog
from Data.project_documents import Stage
from Data.studio_documents import Project, User
from Gui.abstract_widgets.context_menu_widget import ContextMenuWidget
from Gui.user_widgets.user_list.user_list_view import UserListView


class UserSelectMenu(ContextMenuWidget):
    project = app_dialog.get_project()
    users = project.users

    def __init__(self, stage: Stage):
        super().__init__(w=168, h=248)
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

    def on_user_selected(self, pseudo: str):
        user = User.objects.get(pseudo=pseudo)
        self.stage.set_user(user)
        self.close()
