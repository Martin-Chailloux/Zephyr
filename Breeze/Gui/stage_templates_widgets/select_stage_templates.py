import qtawesome
from PySide6 import QtCore
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QPushButton

from Data.project_documents import StageTemplate, Asset
from Dialogs.breeze_dialog import create_stage
from Gui.popups.line_edit_popup import LineEditPopup
from Gui.stages_widgets.stage_item import StageButton
from Gui.util_widgets.util_widgets import IconButton


class StageTemplateSelector(QDialog):
    def __init__(self, asset: Asset):
        super().__init__()
        self.asset = asset
        self.templates: list[StageTemplate] = StageTemplate.objects()

        self.setWindowTitle("Stage templates")

        self._init_ui()
        self.connect_signals()
        self.refresh()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(3)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)

        # ---------------
        # Presets settings
        # ---------------
        label = QLabel("Preset")
        layout.addWidget(label)

        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)

        presets_cb = QComboBox()
        h_layout.addWidget(presets_cb)

        w = presets_cb.sizeHint().height()

        save_button = IconButton(icon_name="mdi6.content-save", width=w)
        h_layout.addWidget(save_button)
        save_button.setToolTip("Save preset")

        save_as_button = IconButton(icon_name="mdi6.content-save-plus", width=w)
        h_layout.addWidget(save_as_button)
        save_as_button.setToolTip("Save as new preset")

        layout.addSpacing(7)

        # ---------------
        # Stage templates
        # ---------------
        self.buttons = []
        for template in self.templates:
            button = StageButton(template=template)
            layout.addWidget(button)
            self.buttons.append(button)
            button.template = template

        layout.addSpacing(7)

        # ---------------
        # Buttons
        # ---------------
        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)

        cancel_button = QPushButton("Cancel")
        cancel_button.setIcon(qtawesome.icon("fa.close"))
        confirm_button = QPushButton("Confirm")
        confirm_button.setIcon(qtawesome.icon("fa.check"))
        for button in [cancel_button, confirm_button]:
            h_layout.addWidget(button)

        # ---------------
        # Public vars
        # ---------------
        self.presets_cb = presets_cb
        self.save_button = save_button
        self.save_as_button = save_as_button

        self.cancel_button = cancel_button
        self.confirm_button = confirm_button

    def connect_signals(self):
        self.presets_cb.currentIndexChanged.connect(self.on_presets_cb_index_changed)

        self.save_button.clicked.connect(self.on_save)
        self.save_as_button.clicked.connect(self.on_save_as)

        self.cancel_button.clicked.connect(self.close)
        self.confirm_button.clicked.connect(self.on_confirm)

    @property
    def presets(self) -> list[str]:
        presets = [self.presets_cb.itemText(i) for i in range(self.presets_cb.count())]
        return presets

    def refresh(self):
        presets: list[str] = []
        for template in self.templates:
            for preset in template.presets:
                if preset not in presets:
                    presets.append(preset)
        presets.sort()
        self.presets_cb.clear()
        self.presets_cb.addItems(presets)

        self.on_presets_cb_index_changed()

    def on_presets_cb_index_changed(self):
        enable_save = self.presets_cb.count() > 0
        self.save_button.setEnabled(enable_save)

        preset = self.presets_cb.currentText()
        for button in self.buttons:
            button.setChecked(preset in button.template.presets)

    def on_save(self):
        preset = self.presets_cb.currentText()

        for button in self.buttons:
            template = button.template
            if button.isChecked():
                if preset not in template.presets:
                    template.presets.append(preset)
            elif preset in template.presets:
                template.presets.remove(preset)
            button.template.save()

        self.refresh()
        if preset in self.presets:
            self.presets_cb.setCurrentText(preset)

    def on_save_as(self):
        popup = LineEditPopup(title="New preset",
                              invalid_entries=self.presets,
                              close_on_confirm=True)
        popup.create_clicked.connect(self.create_preset)
        popup.exec()

    def on_confirm(self):
        templates = [button.template for button in self.buttons if button.isChecked()]
        names = [template.name for template in templates]
        existing_stage_names = [stage.stage_template.name for stage in self.asset.stages]
        names = [n for n in names if n not in existing_stage_names]

        stage_templates: list[StageTemplate] = [StageTemplate.objects.get(name=name) for name in names]

        for stage_template in stage_templates:
            stage = create_stage(stage_template=stage_template, asset=self.asset)

        self.close()

    def create_preset(self, preset: str):
        self.presets_cb.blockSignals(True)
        self.presets_cb.addItem(preset)
        self.presets_cb.setCurrentText(preset)
        self.presets_cb.blockSignals(False)
        self.on_save()
