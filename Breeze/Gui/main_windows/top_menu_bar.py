from typing import Callable

import qtawesome
from PySide6 import QtCore
from PySide6.QtCore import QSize, Signal
from PySide6.QtGui import QAction, QKeySequence, QActionEvent, QPaintEvent, QPainter, QBrush, QColor, QPixmap, QImage, \
    QIcon
from PySide6.QtWidgets import QMenuBar, QMenu, QWidget, QHBoxLayout, QLabel, QVBoxLayout, QSizePolicy, QPushButton, \
    QStackedWidget, QGridLayout

from Api.breeze_app import BreezeApp
from Api.document_models.studio_documents import User
from Gui.popups.user_editor import UserEditor
from Utils.user_widgets import UserPicture

modifiers = QtCore.Qt.Modifier
keys = QtCore.Qt.Key


class BreezeTopMenuBar(QWidget):
    project_changed = Signal()

    def __init__(self):
        super().__init__()
        self._init_ui()
        self._connect_signals()
        self._init_state()

    def _init_ui(self):
        # settings_menu = self.add_menu(self, label="Settings", icon_name="fa.gear")  # Not needed yet
        """
        A grid layout is used to have custom buttons on top of a default menu_bar, on its right
        """
        grid = QGridLayout()
        self.setLayout(grid)
        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)

        # ------------------------
        # left side
        # ------------------------
        l_layout = QHBoxLayout()
        grid.addLayout(l_layout, 0, 0, QtCore.Qt.AlignmentFlag.AlignLeft)

        menu_bar = QMenuBar()
        l_layout.addWidget(menu_bar)

        palette_menu = self.add_menu(menu_bar, label="Palette", icon_name="fa5s.palette")
        project_menu = self.add_menu(menu_bar, label="Project", icon_name="ri.landscape-fill")
        help_menu = self.add_menu(menu_bar, label="Help", icon_name="fa.question")

        self.add_action(palette_menu, label="Breeze")
        self.add_action(palette_menu, label="Dark")
        self.add_action(palette_menu, label="Light")

        self.add_action(project_menu, label="Change")
        self.add_action(project_menu, label="Edit", shortcut=keys.Key_U)

        # ------------------------
        # right side
        # ------------------------
        r_layout = QHBoxLayout()
        grid.addLayout(r_layout, 0, 0, QtCore.Qt.AlignmentFlag.AlignRight)

        project_edit = QPushButton(' Project ')
        r_layout.addWidget(project_edit)

        user_edit = QPushButton()
        r_layout.addWidget(user_edit)
        h = 28
        user_edit.setFixedSize(QSize(h, h))
        user_edit.setIconSize(QSize(h, h))

        self.project_edit = project_edit
        self.user_edit = user_edit

    def _connect_signals(self):
        self.user_edit.clicked.connect(self.on_user_edited)
        self.project_edit.clicked.connect(self.on_project_edited)

    def _init_state(self):
        self.set_user(user=BreezeApp.user)

    def set_user(self, user: User):
        image = QImage(user.icon_path)
        pixmap = QPixmap.fromImage(image)
        icon = QIcon(pixmap)
        self.user_edit.setIcon(icon)

        print(f"SET USER: {user}")

    def on_project_edited(self):
        BreezeApp.set_project(name='empty')
        self.project_changed.emit()  # unintuitive for the menubar to know about this, but it works for now

    def on_user_edited(self):
        editor = UserEditor()
        editor.exec()
        self._init_state()  # hack to update the gui

    def add_menu(self, parent: QMenuBar | QMenu, label: str, icon_name: str) -> QMenu:
        # TODO: tooltips are not working
        #  not needed for now
        menu = QMenu(label, self)
        parent.addMenu(menu)
        # menu.setIcon(qtawesome.icon(icon_name))
        menu.setStyleSheet("QMenu::item {padding: 4px 12px 4px 12px;}")

        return menu

    def add_action(self, parent: QMenuBar | QMenu, label: str, icon_name: str=None, shortcut: QtCore.Qt.Key|QKeySequence=None) -> QAction:
        action = QAction(label, self)
        parent.addAction(action)
        if icon_name is not None:
            action.setIcon(qtawesome.icon(icon_name))
        # if shortcut is not None:
        #     action.setShortcut(shortcut)
        # action.setShortcutVisibleInContextMenu(False)

        return action

    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)
        # TODO: paint a user picture with hover and press behavior over a QPushButton