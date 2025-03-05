import qtawesome

from PySide6 import QtCore
from PySide6.QtCore import Signal, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy, QComboBox)

from MangoEngine.document_models import Status, StageTemplate, Asset, Stage
from MangoEngine.mongo_dialog import create_stage
from Widgets.stage_widgets import StageTemplateSelector, StageButton
from Widgets.status_widgets import StatusSelectWidget


class StageItem(QWidget):
    h = 28
    stage_selected = Signal(str)

    def __init__(self, stage: Stage):
        self.stage = stage
        super().__init__()

        self._init_ui()
        self.connect_signals()

    def __repr__(self):
        return f"StageItem|{self.stage.__repr__()}"

    def set_stage(self, stage: Stage):
        while self.layout().count():
            item = self.layout().takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.stage = stage
        self._init_ui()
        self.connect_signals()

    def _init_ui(self):
        # TODO: le layout se set pas une 2e fois si on rappelle la fonction
        #   donc on utilise self.layout() ensuite
        #   lire la doc Qt pour comprendre
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.setFixedHeight(self.h)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        # TODO: photo de profil comme icone, le nom en tooltip quand on hover
        # TODO: bigger round button with tooltip
        # TODO: offset in its own widget
        user_combobox = QComboBox()
        self.layout().addWidget(user_combobox)
        user_combobox.setFixedHeight(self.h)
        users = ["Martin", "Kim", "Elise", "Chloé", "Hugo", "Camille"]
        user_combobox.addItems(users)
        for i, user in enumerate(users):
            icon_path = f"Icons/Users/{user.lower()}.jpg"
            icon = QIcon(icon_path)
            user_combobox.setItemIcon(i, icon)
            user_combobox.setToolTip("UserTest")

        button = StageButton(template=self.stage.stage_template, h=self.h)
        self.layout().addWidget(button)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        status_button = StatusSelectWidget(height=self.h)
        self.layout().addWidget(status_button)

        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # public vars
        self.button = button

    def connect_signals(self):
        self.button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        if self.button.isChecked():
            self.stage_selected.emit(self.stage.longname)



class StageListWidget(QWidget):
    stage_selected = Signal(str)
    margin: int = 7

    def __init__(self):
        super().__init__()
        self.asset: Asset = None
        self.stage_items: list[StageItem] = []
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(self.margin, self.margin, self.margin, self.margin)
        layout.setSpacing(5)

        stages_layout = QVBoxLayout()
        layout.addLayout(stages_layout)
        stages_layout.setContentsMargins(3, 3, 3, 3)

        # 'Edit' button
        edit_button = QPushButton(" Edit stages")
        layout.addWidget(edit_button)
        edit_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        edit_button.setIcon(qtawesome.icon("mdi.format-list-checkbox"))
        edit_button.setIconSize(QSize(22, 22))
        edit_button.clicked.connect(self.on_edit_stages_clicked)

        edit_button.setFixedHeight(26)

        # public vars
        self.stage_layout = stages_layout
        self.new_button = edit_button

    def set_asset(self, asset: Asset):
        self.asset = asset
        self.refresh_stage_items()

    def clear_stage_items(self):
        self.stage_items = []
        while self.stage_layout.count():
            item = self.stage_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.clear_stage_items()

    def refresh_stage_items(self):
        # TODO: sort by order
        # TODO: cache selection for each asset (use longname as key)
        self.clear_stage_items()
        stages: list[Stage] = self.asset.stages

        for stage in stages:
            self.add_stage_item(stage)

    def add_stage_item(self, stage: Stage):
        stage_item = StageItem(stage=stage)
        self.stage_layout.addWidget(stage_item)
        stage_item.stage_selected.connect(self.on_stage_selected)

        self.stage_items.append(stage_item)

    # ------------------------
    # Events
    # ------------------------
    def on_edit_stages_clicked(self):
        popup = StageTemplateSelector()
        popup.confirmed.connect(self.on_preset_applied)
        popup.exec()

    def on_preset_applied(self, templates_string: str):
        names: list[str] = templates_string.split("_")
        existing_stage_names = [stage.stage_template.name for stage in self.asset.stages]
        names = [n for n in names if n not in existing_stage_names]

        stage_templates: list[StageTemplate] = [StageTemplate.objects.get(name=name) for name in names]

        for stage_template in stage_templates:
            create_stage(stage_template=stage_template, asset=self.asset)

        self.refresh_stage_items()

    def on_stage_selected(self, longname: str):
        # uncheck other stages
        sender: StageItem = self.sender()
        for i, stage_item in enumerate(self.stage_items):
            if stage_item is not sender:
                stage_item.button.setChecked(False)

        # TODO: get_asset(), get_stage(), etc.
        self.stage_selected.emit(longname)
