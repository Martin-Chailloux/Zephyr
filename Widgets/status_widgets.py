from textwrap import dedent

from PySide6.QtCore import QPoint, QSize, Signal
from PySide6.QtGui import QColor, QCursor
from PySide6.QtWidgets import QPushButton, QGridLayout
from qtpy.QtWidgets import QMenu

from Gui.palette_api import ZPalette

c = ZPalette()

class ZStatusSelector(QPushButton):
    # TODO: les choix doivent venir de la db
    # TODO: disabled style

    colors = {
        "WAIT": c.text_white,
        "TODO": c.yellow,
        "WIP": c.orange,
        "WFA": c.purple,
        "DONE": c.green,
        "ERROR": c.red,
        "OMIT": c.light,
    }

    w: int = 46

    def __init__(self, height: int = 26, starting_status: str = "TODO"):
        super().__init__()
        self.h = height
        self.setFixedSize(self.w, self.h)
        self.set_new_status(text=starting_status)

    def set_new_status(self, text: str):
        success = False
        for name, color in self.colors.items():
            if text == name:
                self.setText(text)
                set_stylesheet(self, color)
                success = True
        if not success:
            raise ValueError("Unknown status, cannot set.")

    def mousePressEvent(self, event):
        self.create_menu()

    def create_menu(self):
        menu = SelectStatusMenu(button_w = self.w, button_h = self.h + 8)
        menu.status_selected.connect(self.set_new_status)

        x = int(QCursor.pos().x() - menu.w / 2)
        y = int(QCursor.pos().y() - menu.h / 2)
        menu.exec(QPoint(x, y))


class SelectStatusMenu(QMenu):
    margin = 10
    spacing = 1
    max_columns: int = 2
    status_selected = Signal(str)

    colors = {
        "TODO": c.yellow,
        "WIP": c.orange,
        "WFA": c.purple,
        "DONE": c.green,
        "WAIT": c.text_white,
        "ERROR": c.red,
        "OMIT": c.light,
    }

    def __init__(self, button_w: int, button_h: int):
        super().__init__()
        self.max_rows = int(len(self.colors) / self.max_columns)

        layout = QGridLayout()
        self.setLayout(layout)
        layout.setContentsMargins(self.margin, self.margin, self.margin, self.margin)
        layout.setSpacing(self.spacing)

        self.w = (button_w * self.spacing * self.max_columns) + (2 * self.margin)
        self.h = (button_h * self.spacing * self.max_rows) + (2 * self.margin)
        self.setFixedSize(QSize(self.w, self.h))

        for i, (text, color) in enumerate(self.colors.items()):
            button = QPushButton(text)
            set_stylesheet(button, color)
            button.clicked.connect(self.on_button_clicked)

            row = int(i / self.max_columns)
            column = i % self.max_columns
            layout.addWidget(button, row, column)

    def on_button_clicked(self):
        button: QPushButton = self.sender()
        self.status_selected.emit(button.text())
        self.close()


def set_stylesheet(widget, color: QColor):
    c_base = color.name()
    c_hover = color.lighter(110).name()
    widget.setStyleSheet(dedent("""
                    QPushButton {
                        color: black ;
                        background-color:$c_base;
                        border: 2px solid transparent;
                    }
                    QPushButton:hover {
                        background-color:$c_hover;
                        border: none;
                    }
                    """)
                    .replace("$c_base", c_base)
                    .replace("$c_hover", c_hover))