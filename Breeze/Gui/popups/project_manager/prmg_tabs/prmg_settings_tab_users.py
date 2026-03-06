import time
from typing import Optional

import qtawesome
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel

from Api.breeze_app import BreezeApp
from Api.document_models.project_documents import SubUser
from Api.document_models.studio_documents import Project
from Gui.mvd.user_mvd.user_list_view import UserListView


class ProjectSettingsUsersTab(QWidget):
    def __init__(self):
        super().__init__()
        self.project: Optional[Project] = None
        self._init_ui()
        self._connect_signals()
        self._init_state()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # ------------------------
        # users
        # ------------------------
        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)

        # available users
        v_layout = QVBoxLayout()
        h_layout.addLayout(v_layout)

        v_layout.addWidget(QLabel('Available'))

        available_users = UserListView()
        v_layout.addWidget(available_users)

        # working users
        v_layout = QVBoxLayout()
        h_layout.addLayout(v_layout)

        v_layout.addWidget(QLabel('Working'))

        working_users = UserListView()
        v_layout.addWidget(working_users)

        # ------------------------
        # buttons
        # ------------------------
        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)
        h_layout.setSpacing(3)

        cancel_button = QPushButton()
        h_layout.addWidget(cancel_button)
        cancel_button.setIcon(qtawesome.icon('fa.close'))
        cancel_button.setFixedSize(QSize(28, 28))
        cancel_button.setToolTip('Cancel')

        confirm_button = QPushButton('Accept')
        h_layout.addWidget(confirm_button)
        confirm_button.setIcon(qtawesome.icon('fa.check'))
        confirm_button.setFixedHeight(28)

        self.available_users = available_users
        self.working_users = working_users
        self.cancel_button = cancel_button
        self.confirm_button = confirm_button

    def _connect_signals(self):
        self.available_users.selectionModel().selectionChanged.connect(self.on_available_user_selected)
        self.working_users.selectionModel().selectionChanged.connect(self.on_working_user_selected)
        self.cancel_button.clicked.connect(self.refresh)
        self.confirm_button.clicked.connect(self.confirm)

    def _init_state(self):
        self.refresh()

    def refresh(self):
        self.block_signals(True)

        self.available_users.set_available_users()
        self.working_users.set_sub_users()

        self.block_signals(False)

        self.cancel_button.setEnabled(False)
        self.confirm_button.setEnabled(False)

    def block_signals(self, block: bool):
        self.available_users.selectionModel().blockSignals(block)
        self.working_users.selectionModel().blockSignals(block)

    def swap_user(self, source: UserListView, target: UserListView):
        self.block_signals(block=True)

        user = source.get_user()

        source_users = [x for x in source.users if x != user]
        source.set_users(users=source_users)

        target_users = target.users
        if user not in target_users:
            target_users.append(user)
            target.set_users(users=target_users)

        self.block_signals(block=False)

        self.cancel_button.setEnabled(True)
        self.confirm_button.setEnabled(True)

    def on_available_user_selected(self):
        self.swap_user(source=self.available_users, target=self.working_users)

    def on_working_user_selected(self):
        self.swap_user(source=self.working_users, target=self.available_users)

    def confirm(self):
        working_users = self.working_users.users

        # delete old SubUsers
        sub_users: list[SubUser] = SubUser.objects()
        for sub_user in sub_users:
            if sub_user.source_user not in working_users:
                current_user = BreezeApp.user
                if sub_user.source_user == current_user:
                    raise ValueError(f"Cannot remove {current_user} from the project because it is currently online.")
                sub_user.set_omit(is_omit=True)

        # create new SubUsers
        for user in working_users:
            sub_user = SubUser.from_pseudo(pseudo=user.pseudo)
            if sub_user is None:
                SubUser.create_for_user(pseudo=user.pseudo)
            elif sub_user.is_omit:
                sub_user.set_omit(is_omit=False)

        self.refresh()

    def set_project(self, project: Optional[Project]):
        self.project = project
