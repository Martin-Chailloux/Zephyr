import qtawesome

from PySide6 import QtCore
from PySide6.QtCore import Signal, QSize
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QSizePolicy)

from Data.breeze_documents import StageTemplate, Asset, Stage
from Dialogs.breeze_dialog import create_stage
from Gui.stage_templates_widgets.select_stage_templates import StageTemplateSelector
from Gui.stage_widgets.stage_subwidgets import StageItem


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
