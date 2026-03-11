from datetime import date

import qtawesome
from PySide6 import QtCore
from PySide6.QtCore import QDate
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QHBoxLayout, QPushButton,
                               QLabel, QComboBox, QDateEdit, QProgressBar)

from Breeze.Api.breeze_app import BreezeApp


class ProjectSettingsGeneralTab(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._connect_signals()
        self._init_state()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # ------------------------
        # form
        # ------------------------
        form = QFormLayout()
        layout.addLayout(form)

        root_path_widget = _RootPathWidget()
        resolution_widget = _ResolutionWidget()
        start_widget = _DateWidget()
        end_widget = _DateWidget()
        for date_widget in [start_widget, end_widget]:
            date_widget.setDisplayFormat('dd/MM/yyyy')
        progression_widget = _InteractiveProgressBarWidget()
        status_widget = QLabel('Wip')

        form.addRow("root path", root_path_widget)
        form.addRow("resolution", resolution_widget)
        form.addRow("start", start_widget)
        form.addRow("end", end_widget)
        form.addRow("progress", progression_widget)
        form.addRow('status', status_widget)

        # ------------------------
        # submit buttons
        # ------------------------
        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)
        h_layout.setSpacing(3)
        h_layout.setContentsMargins(0, 0, 0, 0)

        reset_button = QPushButton('Reset')
        h_layout.addWidget(reset_button)

        confirm_button = QPushButton('Confirm')
        h_layout.addWidget(confirm_button)

        for button in [reset_button, confirm_button]:
            button.setFixedHeight(28)

        self.progression = progression_widget
        self.resolution = resolution_widget
        self.start_date = start_widget
        self.end_date = end_widget

    def _connect_signals(self):
        self.progression.valueChanged.connect(self.update_progression)
        self.resolution.currentTextChanged.connect(self.update_resolution)
        self.start_date.dateTimeChanged.connect(self.update_start_date)
        self.end_date.dateChanged.connect(self.update_end_date)

    def _init_state(self):
        self.refresh()

    def refresh(self):
        self.progression.setValue(BreezeApp.project.progression)
        self.resolution.set_resolution(BreezeApp.project.res)
        self.start_date.set_date(source_date=BreezeApp.project.start_date)
        self.end_date.set_date(source_date=BreezeApp.project.end_date)

    def update_progression(self):
        BreezeApp.project.set_progression(progression=self.progression.value())

    def update_resolution(self):
        res = self.resolution.get_resolution()
        BreezeApp.project.set_resolution(res[0], res[1])

    def update_start_date(self):
        BreezeApp.project.set_start_date(start_date=self.start_date.get_date())

    def update_end_date(self):
        BreezeApp.project.set_end_date(end_date=self.end_date.get_date())


class _RootPathWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._connect_signals()
        self._init_state()

    def _init_ui(self):
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(3)
        layout.setContentsMargins(0, 0, 0, 0)

        field = QLineEdit()
        layout.addWidget(field)
        field.setPlaceholderText("path")

        file_dialog_button = QPushButton()
        layout.addWidget(file_dialog_button)
        file_dialog_button.setIcon(qtawesome.icon('fa.folder'))
        file_dialog_button.setFixedHeight(field.sizeHint().height())

    def _connect_signals(self):
        pass

    def _init_state(self):
        pass


class _ResolutionWidget(QComboBox):
    presets: dict[str, list[int]] = {
        'Full HD (1920x1080)': [1920, 1080],
        'Cinemascope (2048x858)': [2048, 858],
    }

    def __init__(self):
        super().__init__()
        self.addItems([text for text in self.presets.keys()])

    def get_resolution(self) -> list[int]:
        res = self.presets[self.currentText()]
        return res

    def set_resolution(self, res: list[int]):
        for preset_text, preset_res in self.presets.items():
            if preset_res == res:
                self.setCurrentText(preset_text)
                return
        else:
            f"Did not find a preset with resolution: {res}"


class _DateWidget(QDateEdit):
    def get_date(self) -> date:
        year, month, day = self.date().getDate()
        return date(year, month, day)

    def set_date(self, source_date: date):
        if source_date is None:
            return
        year, month, day = source_date.year, source_date.month, source_date.day
        self.setDate(QDate(year, month, day))


class _InteractiveProgressBarWidget(QProgressBar):
    def __init__(self):
        super().__init__()
        self.setMaximum(100)

    def set_value(self, event):
        x = event.pos().x()
        w = self.width()
        percent = x/w * 100
        self.setValue(int(percent))

    def mouseMoveEvent(self, event):
        if QtCore.Qt.MouseButton.LeftButton in event.buttons():
            self.set_value(event=event)
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        self.set_value(event=event)
        super().mousePressEvent(event)
