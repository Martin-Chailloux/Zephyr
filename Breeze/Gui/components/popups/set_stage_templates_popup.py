import qtawesome
from PySide6 import QtCore
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton

from Api.project_documents import Asset, Stage
from Gui.components.mvd.stage_template_mvd.stage_template_list_view import StageTemplateListView
from Gui.components.popups.abstract_popup_widget import AbstractPopupWidget
from Gui.components.popups.line_edit_popup import LineEditPopup
from Gui.sub_widgets.stage_templates_widgets.stage_template_presets_bar import StageTemplatesPresetsBar


class SetStageTemplatesPopup(AbstractPopupWidget):
    def __init__(self, asset: Asset):
        super().__init__(w=280, h=560, show_borders=True, position=[0.5, 1])
        self.asset = asset

        self.setWindowTitle("Assign stage templates")

        self._init_ui()
        self._connect_signals()
        self.refresh_presets()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(3)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)

        # presets
        presets_bar = StageTemplatesPresetsBar()
        layout.addWidget(presets_bar)
        layout.addSpacing(7)

        # stage templates list
        stage_templates_list = StageTemplateListView()
        layout.addWidget(stage_templates_list)

        # buttons
        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)

        cancel_button = QPushButton("Cancel")
        cancel_button.setIcon(qtawesome.icon("fa.close"))

        confirm_button = QPushButton("Confirm")
        confirm_button.setIcon(qtawesome.icon("fa.check"))

        for button in [cancel_button, confirm_button]:
            h_layout.addWidget(button)

        # public vars
        self.presets_bar = presets_bar
        self.stage_templates_list = stage_templates_list
        self.cancel_button = cancel_button
        self.confirm_button = confirm_button

    def _connect_signals(self):
        self.presets_bar.combobox.currentIndexChanged.connect(self.on_presets_combobox_index_changed)
        self.presets_bar.save_button.clicked.connect(self.on_preset_saved)
        self.presets_bar.save_as_button.clicked.connect(self.on_preset_saved_as)

        self.cancel_button.clicked.connect(self.close)
        self.confirm_button.clicked.connect(self.on_confirm)

        self.stage_templates_list.right_clicked.connect(self.reject)

    def refresh_presets(self):
        # collect each existing preset once
        presets: list[str] = []
        for template in self.stage_templates_list.stage_templates:
            for preset in template.presets:
                if preset not in presets:
                    presets.append(preset)

        # fill the combobox
        presets.sort()
        self.presets_bar.combobox.clear()
        self.presets_bar.combobox.addItems(presets)

        # can only save when there is at least one preset
        can_save = self.presets_bar.combobox.count() > 0
        self.presets_bar.save_button.setEnabled(can_save)

    @property
    def presets(self) -> list[str]:
        presets = [self.presets_bar.combobox.itemText(i) for i in range(self.presets_bar.combobox.count())]
        return presets

    def on_presets_combobox_index_changed(self):
        preset = self.presets_bar.combobox.currentText()
        self.stage_templates_list.set_preset(preset=preset)

    def on_preset_saved(self):
        # save in db
        preset = self.presets_bar.combobox.currentText()
        self.stage_templates_list.save_preset(preset=preset)

        # set in combobox
        self.refresh_presets()
        if preset in self.presets:
            self.presets_bar.combobox.setCurrentText(preset)

    def on_preset_saved_as(self):
        popup = LineEditPopup(title="New preset",
                              invalid_entries=self.presets,
                              close_on_confirm=True)
        popup.create_clicked.connect(self.create_preset)
        popup.exec()

    def create_preset(self, preset: str):
        self.presets_bar.combobox.blockSignals(True)
        self.presets_bar.combobox.addItem(preset)
        self.presets_bar.combobox.setCurrentText(preset)
        self.presets_bar.combobox.blockSignals(False)
        self.on_preset_saved()

    def on_confirm(self):
        stage_templates = self.stage_templates_list.selected_stage_templates
        existing_stage_templates = [stage.stage_template for stage in self.asset.stages]

        for stage_template in stage_templates:
            if stage_template not in existing_stage_templates:
                Stage.create(stage_template=stage_template, asset=self.asset)

        self.close()
