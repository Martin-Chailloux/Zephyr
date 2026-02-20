import qtawesome
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel

from Api.document_models.project_documents import SubUser
from Gui.mvd.user_mvd.user_list_view import UserListView


class ProjectSettingsUsersTab(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._connect_signals()
        self._init_state()

    def _init_ui(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        # available
        v_layout = QVBoxLayout()
        layout.addLayout(v_layout)

        v_layout.addWidget(QLabel('Available'))

        available_users = UserListView()
        v_layout.addWidget(available_users)

        # working
        v_layout = QVBoxLayout()
        layout.addLayout(v_layout)

        v_layout.addWidget(QLabel('Working'))

        working_users = UserListView()
        v_layout.addWidget(working_users)

        # add_button = QPushButton('Add')
        # layout.addWidget(add_button)
        # add_button.setIcon(qtawesome.icon('fa.plus-circle'))
        # add_button.setFixedHeight(28)

        self.available_users = available_users
        self.working_users = working_users

    def _connect_signals(self):
        self.available_users.selectionModel().selectionChanged.connect(self.on_available_user_selected)
        self.working_users.selectionModel().selectionChanged.connect(self.on_working_user_selected)

    def _init_state(self):
        self.refresh()

    def refresh(self):
        self.available_users.selectionModel().blockSignals(True)
        self.working_users.selectionModel().blockSignals(True)

        self.available_users.set_available_users()
        self.working_users.set_sub_users()

        self.available_users.selectionModel().blockSignals(False)
        self.working_users.selectionModel().blockSignals(False)

    def on_available_user_selected(self):
        user = self.available_users.get_user()
        # hack to create a SubUser if it does not exist
        _ = SubUser.from_pseudo(pseudo=user.pseudo, create_if_missing=True)
        self.refresh()

    def on_working_user_selected(self):
        user = self.working_users.get_sub_user()
        user.delete()
        self.refresh()
