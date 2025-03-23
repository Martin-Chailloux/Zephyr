from textwrap import dedent

from PySide6 import QtCore
from PySide6.QtCore import QSize, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QPushButton, QGridLayout

from Data import status
from Dialogs.palette_dialog import Palette
from Utils.util_widgets.util_widgets import ContextMenuWidget


class SelectStatusWidget(QPushButton):
    palette: Palette = Palette.objects.get(name="dev")
    statuses = status.default_statuses

    w: int = 48

    def __init__(self, height: int = 26, starting_status: str = "TODO"):
        super().__init__()
        self.h = height
        self.setFixedSize(self.w, self.h)
        self.set_new_status(text=starting_status)

    def set_new_status(self, text: str):
        success = False
        for _status in self.statuses:
            if text == _status.label:
                self.setText(text)
                set_stylesheet(self, _status.color)
                success = True
        if not success:
            raise ValueError("Unknown status, cannot set.")

    def mousePressEvent(self, event):
        self.create_menu()

    def create_menu(self):
        menu = SelectStatusMenu()
        menu.status_selected.connect(self.set_new_status)
        menu.exec()


class SelectStatusMenu(ContextMenuWidget):
    palette: Palette = Palette.objects.get(name="dev")

    status_selected = Signal(str)

    margin = 2
    spacing = 1
    button_w = 48
    button_h = 28
    max_columns = 2

    statuses = status.default_statuses

    def __init__(self):
        max_rows = int(len(self.statuses) / self.max_columns) + 1
        w = (self.button_w * self.max_columns) + (2 * self.margin)
        h = (self.button_h * max_rows) + (2 * self.margin)

        super().__init__(w=w, h=h,
                         align_h=QtCore.Qt.AlignmentFlag.AlignHCenter,
                         align_v=QtCore.Qt.AlignmentFlag.AlignVCenter)
        self._init_ui()

    def _init_ui(self):
        layout = QGridLayout()
        self.setLayout(layout)
        layout.setContentsMargins(self.margin, self.margin, self.margin, self.margin)
        layout.setSpacing(self.spacing)

        for i, _status in enumerate(self.statuses):
            button = QPushButton(_status.label)
            set_stylesheet(button, _status.color)
            button.clicked.connect(self.on_button_clicked)
            button.setFixedSize(QSize(self.button_w, self.button_h))

            row = int(i / self.max_columns)
            column = i % self.max_columns
            layout.addWidget(button, row, column)

    def on_button_clicked(self):
        # TODO: subclass button to send more infos than label
        button: QPushButton = self.sender()
        _status: str = button.text()
        self.status_selected.emit(_status)
        print(f"Selected status: {_status}")
        self.close()


def set_stylesheet(widget, color: str):
    hover_color = QColor(color).lighter(110).name()
    widget.setStyleSheet(dedent("""
                    QPushButton {
                        color: black ;
                        background-color: $color;
                        border: 2px solid transparent;
                    }
                    QPushButton:hover {
                        background-color: $hover_color;
                        border: none;
                    }
                    """)
                    .replace("$color", color)
                    .replace("$hover_color", hover_color))
