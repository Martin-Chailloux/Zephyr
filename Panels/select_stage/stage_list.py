import qtawesome

from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QHBoxLayout,
                               QSizePolicy, QComboBox)

from MangoEngine.document_models import Status
from Widgets.line_edit_popup import LineEditPopup
from Widgets.qwidgets_extensions import ZIconButton, ZTransparentIconButton
from Widgets.status_widgets import ZStatusComboBox


class StageItem(QWidget):
    h = 26
    moved = Signal()
    def __init__(self, name: str, status: str):
        self.name = name
        self.status = status
        super().__init__()

        self._init_ui()

    def __repr__(self):
        return f"StageItem|{self.name}"

    def _init_ui(self):
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.setFixedHeight(self.h)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        # mover = ZIconButton(icon_name="mdi.arrow-up-bold", width=self.h, icon_size=18)
        mover = ZTransparentIconButton(icon_name="mdi.arrow-up-bold", width=self.h, icon_size=18)
        mover.clicked.connect(self.moved.emit)
        layout.addWidget(mover)

        button = QPushButton(self.name)
        layout.addWidget(button)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        button.setCheckable(True)

        # TODO: photo de profil comme icone, le nom en tooltip quand on hover
        user_combobox = QComboBox()
        layout.addWidget(user_combobox)
        users = ["Martin", "Kim", "Elise", "Chloé", "Hugo", "Camille"]
        user_combobox.addItems(users)

        status = ZStatusComboBox(starting_status=self.status)
        layout.addWidget(status)

        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # for widget in [user_combobox, status]:
        #     # widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        #     widget.setFixedHeight(self.h + 12)

        # public vars
        self.mover = mover


class ZStageListWidget(QWidget):
    defaults = {
        "modeling": [],
        "rigging": [],
        "texturing": [],
        "shading": [],
    }

    create_stage_request = Signal(str)
    margin: int = 7

    def __init__(self):
        super().__init__()
        self.stage_items: list[StageItem] = []

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(self.margin, self.margin, self.margin, self.margin)
        layout.setSpacing(5)

        new_button = QPushButton(" New stage")
        layout.addWidget(new_button)
        new_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        new_button.setIcon(qtawesome.icon("fa.plus-circle"))
        new_button.clicked.connect(self.create_popup)
        self.new_button = new_button

        for stage_name in self.defaults.keys():
            self.add_stage_item(stage_name, Status.WFA)

    def add_stage_item(self, name, status=Status.TODO):
        stage_item = StageItem(name=name, status=status)
        self.layout().addWidget(stage_item)
        self.layout().insertWidget(-1, self.new_button)

        stage_item.moved.connect(self.on_moved_requested)

        self.stage_items.append(stage_item)

    def create_popup(self):
        popup = LineEditPopup(title="New Stage",
                              invalid_entries=[stage_item.name for stage_item in self.stage_items])
        popup.create_clicked.connect(self.add_stage_item)
        popup.exec()

    def crate_stage(self, description: str):
        self.create_stage_request.emit(description)

    def on_moved_requested(self):
        before: list[StageItem] = self.stage_items
        after: list[StageItem] = []

        for i, stage_item in enumerate(self.stage_items):
            sender: StageItem = self.sender()
            if stage_item is sender:
                before = self.stage_items[:i]
                after = self.stage_items[i+1:]
                if  not before:
                    after.append(stage_item)
                else:
                    before.insert(-1, stage_item)

        self.stage_items = before + after
        self.refresh()

    def refresh(self):
        for stage_item in self.stage_items:
            self.layout().addWidget(stage_item)
        self.layout().addWidget(self.new_button)

