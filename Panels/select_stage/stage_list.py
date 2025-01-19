from textwrap import dedent

import qtawesome

from PySide6 import QtCore
from PySide6.QtCore import Signal, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy, QComboBox)

from MangoEngine.document_models import Status
from Widgets.line_edit_popup import LineEditPopup
from Widgets.qwidgets_extensions import ZTransparentIconButton, ZIconButton
from Widgets.status_widgets import ZStatusSelector


class StageItem(QWidget):
    # TODO: paint an icon and a color at the left edge of the item
    h = 26
    moved = Signal()
    stage_selected = Signal(str)

    def __init__(self, name: str, status: str):
        self.name = name
        self.status = status
        super().__init__()

        self._init_ui()
        self.connect_signals()

    def __repr__(self):
        return f"StageItem|{self.name}"

    def _init_ui(self):
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.setFixedHeight(self.h)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        mover = ZTransparentIconButton(icon_name="mdi.arrow-up-bold", width=18, icon_size=18)
        mover.clicked.connect(self.moved.emit)
        layout.addWidget(mover)

        # TODO: photo de profil comme icone, le nom en tooltip quand on hover
        # TODO: bigger round button with tooltip
        user_combobox = QComboBox()
        layout.addWidget(user_combobox)
        user_combobox.setFixedHeight(self.h)
        users = ["Martin", "Kim", "Elise", "Chloé", "Hugo", "Camille"]
        user_combobox.addItems(users)
        for i, user in enumerate(users):
            icon_path = f"Icons/Users/{user.lower()}.jpg"
            icon = QIcon(icon_path)
            user_combobox.setItemIcon(i, icon)
            user_combobox.setToolTip("UserTest")

        button = QPushButton(self.name)
        layout.addWidget(button)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        button.setCheckable(True)
        button.setStyleSheet(dedent("""
            QPushButton {color: darkgrey}
            QPushButton:checked {
                color: white;
                border: 1px solid white;
            }
        """
        ))

        status_button = ZStatusSelector(height=self.h, starting_status=self.status)
        layout.addWidget(status_button)

        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # public vars
        self.mover = mover
        self.button = button

    def connect_signals(self):
        self.button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        if self.button.isChecked():
            text = self.button.text()
            self.stage_selected.emit(text)

class ZStageListWidget(QWidget):
    defaults = {
        "modeling": "ph.cube-fill",
        "rigging": "mdi.human-edit",
        "texturing": "fa.paint-brush",
        "shading": "mdi6.crystal-ball",
    }

    create_stage_request = Signal(str)
    margin: int = 7

    def __init__(self):
        super().__init__()
        self.stage_items: list[StageItem] = []

        self._init_ui()
        self.add_stages()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(self.margin, self.margin, self.margin, self.margin)
        layout.setSpacing(5)

        stage_layout = QVBoxLayout()
        layout.addLayout(stage_layout)
        stage_layout.setContentsMargins(3, 3, 3, 3)

        buttons_layout = QHBoxLayout()
        layout.addLayout(buttons_layout)
        buttons_layout.setSpacing(2)

        h: int = 26
        # 'New' button
        new_button = QPushButton(" Edit")
        buttons_layout.addWidget(new_button)
        new_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        new_button.setIcon(qtawesome.icon("mdi.format-list-checkbox"))
        new_button.setIconSize(QSize(22, 22))
        new_button.clicked.connect(self.create_popup)

        new_button.setFixedHeight(h)

        # public vars
        self.stage_layout = stage_layout
        self.buttons_layout = buttons_layout
        self.new_button = new_button

    def add_stage_item(self, name, status: str=Status.TODO, icon_name: str=None):
        stage_item = StageItem(name=name, status=status)
        if icon_name is not None:
            stage_item.button.setIcon(qtawesome.icon(icon_name))

        self.stage_layout.addWidget(stage_item)
        self.stage_items.append(stage_item)

        stage_item.moved.connect(self.on_moved_requested)
        stage_item.stage_selected.connect(self.on_stage_selected)

    def add_stages(self):
        self.stage_items = []
        for stage_name, icon_name in self.defaults.items():
            self.add_stage_item(name=stage_name, icon_name=icon_name)

    def create_popup(self):
        popup = LineEditPopup(title="New Stage",
                              invalid_entries=[stage_item.name for stage_item in self.stage_items])
        popup.create_clicked.connect(self.add_stage_item)
        popup.exec()

    def crate_stage(self, description: str):
        self.create_stage_request.emit(description)

    def on_moved_requested(self):
        sender: StageItem = self.sender()

        before: list[StageItem] = self.stage_items
        after: list[StageItem] = []

        for i, stage_item in enumerate(self.stage_items):
            if stage_item is sender:
                before = self.stage_items[:i]
                after = self.stage_items[i+1:]
                if  not before:
                    after.append(stage_item)
                else:
                    before.insert(-1, stage_item)

        self.stage_items = before + after
        self.refresh()

    def on_stage_selected(self, stage_name: str):
        print(f"Selected stage: {stage_name}")
        sender: StageItem = self.sender()
        for i, stage_item in enumerate(self.stage_items):
            if stage_item is not sender:
                stage_item.button.setChecked(False)

    def refresh(self):
        for stage_item in self.stage_items:
            self.stage_layout.addWidget(stage_item)

