from textwrap import dedent

from PySide6 import QtCore
from PySide6.QtCore import QRect, Signal
from PySide6.QtGui import QPainter, QBrush, QIcon, QPainterPath, QColor
from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QSizePolicy, QHBoxLayout, QComboBox, QLabel

import qtawesome

from MangoEngine.document_models import StageTemplate
from Widgets.line_edit_popup import LineEditPopup
from Widgets.qwidgets_extensions import ZIconButton


class StageButton(QPushButton):
    unchecked_alpha: float = 0.3

    def __init__(self, template: StageTemplate, h: int=28):
        super().__init__()
        self.template = template
        self.h = h
        self._init_ui()

    def _init_ui(self):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCheckable(True)
        self.setStyleSheet(dedent("""
            QPushButton {color: darkgrey}
            QPushButton:checked {
                color: white;
                border: 1px solid white;
            }
        """))
        self.setFixedHeight(self.h)

        self.setText(self.template.label)

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color = QColor(self.template.color)
        if not self.isChecked():
            color.setAlphaF(self.unchecked_alpha)
        painter.setBrush(QBrush(color))
        painter.setPen("white")

        rect: QRect = event.rect()
        x = rect.x()
        y = rect.y()
        w = rect.width()
        h = rect.height()

        # Fill color
        fill_w = round(w/4)
        rect.setWidth(fill_w)
        border_width = 1
        rect = QRect(x + border_width, y + border_width, fill_w + border_width, h - border_width*2)
        path = QPainterPath()
        path.addRoundedRect(rect, 3, 3)
        painter.fillPath(path, painter.brush())

        # Icon
        margin = 2
        rect.setX(x)
        rect.setY(y+margin)
        rect.setWidth(fill_w)
        rect.setHeight(h - margin*2)

        opacity = 1 if self.isChecked() else self.unchecked_alpha
        icon: QIcon = qtawesome.icon(self.template.icon_name, opacity=opacity)
        icon.paint(painter, rect, QtCore.Qt.AlignmentFlag.AlignRight)

        painter.restore()


class StageTemplateSelector(QDialog):
    confirmed = Signal(str)

    def __init__(self):
        super().__init__()
        self.templates : list[StageTemplate] = StageTemplate.objects()

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

        save_button = ZIconButton(icon_name="mdi6.content-save", width=w)
        h_layout.addWidget(save_button)
        save_button.setToolTip("Save preset")

        save_as_button = ZIconButton(icon_name="mdi6.content-save-plus", width=w)
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
        s = "_".join(name for name in names)
        self.confirmed.emit(s)
        self.close()

    def create_preset(self, preset: str):
        self.presets_cb.blockSignals(True)
        self.presets_cb.addItem(preset)
        self.presets_cb.setCurrentText(preset)
        self.presets_cb.blockSignals(False)
        self.on_save()
