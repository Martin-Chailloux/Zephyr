import qtawesome
from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QHBoxLayout, QPushButton, QLabel, QComboBox, \
    QDateEdit, QProgressBar

from Api.breeze_app import BreezeApp


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
        start_widget = QDateEdit()
        end_widget = QDateEdit()
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

    def _connect_signals(self):
        self.progression.valueChanged.connect(self.update_progression)

    def _init_state(self):
        self.refresh()

    def refresh(self):
        self.progression.setValue(BreezeApp.project.progression)

    def update_progression(self):
        BreezeApp.project.set_progression(progression=self.progression.value())


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


class _ResolutionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._connect_signals()
        self._init_state()

    def _init_ui(self):
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        presets = QComboBox()
        layout.addWidget(presets)
        presets.addItems(['Full HD (1920x1080)', 'Cinemascope (2048x858)'])

    def _connect_signals(self):
        pass

    def _init_state(self):
        pass



class _DateWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._connect_signals()
        self._init_state()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        # layout.setSpacing(3)
        # layout.setContentsMargins(0, 0, 0, 0)

    def _connect_signals(self):
        pass

    def _init_state(self):
        pass


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
