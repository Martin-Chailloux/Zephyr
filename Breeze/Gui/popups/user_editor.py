import qtawesome

from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QFormLayout,
                               QPushButton, QHBoxLayout, QGroupBox)

from Api.breeze_app import BreezeApp
from Api.document_models.studio_documents import User
from Utils.user_widgets import UserPicture


class UserEditor(QDialog):
    user_changed = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowIcon(qtawesome.icon("fa.user"))
        self.setWindowTitle("User editor")
        self._init_ui()
        self._connect_signals()
        self._init_state()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter & QtCore.Qt.AlignmentFlag.AlignCenter)

        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)
        h_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)

        h_layout.addStretch(1)
        user_picture = UserPicture()
        layout.addWidget(user_picture)
        h_layout.addStretch(1)

        user_name = QLabel()
        layout.addWidget(user_name)

        groupbox = QGroupBox("Login")
        layout.addWidget(groupbox)
        v_layout = QVBoxLayout()
        groupbox.setLayout(v_layout)

        form = QFormLayout()
        v_layout.addLayout(form)

        pseudo_input = QLineEdit()
        form.addRow("pseudo", pseudo_input)

        confirm_button = QPushButton("Confirm")
        v_layout.addWidget(confirm_button)

        self.user_picture = user_picture
        self.user_name = user_name
        self.confirm_button = confirm_button
        self.pseudo_input = pseudo_input

    def _connect_signals(self):
        self.confirm_button.clicked.connect(self.on_confirm_clicked)

    def _init_state(self):
        self.set_user(user=BreezeApp.user)

    def on_confirm_clicked(self):
        pseudo_input = self.pseudo_input.text()
        user = User.from_pseudo(pseudo=pseudo_input)
        if user is None:
            raise ValueError(f"User not found from pseudo: {pseudo_input}")
        self.set_user(user=user)
        self.user_changed.emit()

    def set_user(self, user: User):
        self.user_picture.set_user(user)
        self.user_name.setText(user.full_name)
        self.update()

        BreezeApp.set_user(pseudo=user.pseudo)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Return:
            print(f"accept")
            self.on_confirm_clicked()
        elif event.key() == QtCore.Qt.Key.Key_Escape:
            print("reject")
            self.reject()
        else:
            super().keyPressEvent(event)
