from textwrap import dedent

from PySide6 import QtCore
from PySide6.QtCore import QModelIndex, QPoint, QSize, Signal
from PySide6.QtGui import QStandardItemModel, QColor, QCursor
from PySide6.QtWidgets import QComboBox, QListView, QWidget, QVBoxLayout, QPushButton, QDialog, QGridLayout, \
    QHBoxLayout, QSizePolicy
from qtpy.QtWidgets import QMenu

from Gui.palette_api import ZPalette

c = ZPalette()

class ZStatusSelector(QComboBox):
    colors = {
        "WAIT": c.text_white,
        "TODO": c.yellow,
        "WIP": c.orange,
        "WFA": c.purple,
        "DONE": c.green,
        "ERROR": c.red,
        "OMIT": c.light,
    }

    def __init__(self, starting_status: str = "TODO"):
        # TODO: les choix doivent venir de la db
        super().__init__()
        self.addItems([k for k in self.colors.keys()])
        self.view().colors = self.colors

        self.on_text_changed(self.currentText())
        self.currentTextChanged.connect(self.on_text_changed)

        for i, color in enumerate(self.colors.values()):
            self.setItemData(i, color, QtCore.Qt.ItemDataRole.BackgroundRole)
            self.setItemData(i, QColor("black"), QtCore.Qt.ItemDataRole.ForegroundRole)

        if starting_status in self.colors.keys():
            self.setCurrentText(starting_status)

        # self.customContextMenuRequested.connect()

    def on_text_changed(self, text):
        for name, color in self.colors.items():
            color = color.name(format=QColor.NameFormat.HexArgb)
            if text == name:
                self.setStyleSheet(dedent("""
                    QComboBox {
                        background-color: $color;
                        color: black;
                        }
                """.replace("$color", color)))

        unused = """
                    QListView::item:selected {
                        background-color: transparent;
                        color: white;
                        }
        """

    def mousePressEvent(self, event):
        self.create_menu()
        # if event.button() == QtCore.Qt.MouseButton.RightButton:
        # else:
        #     super().mousePressEvent(event)

    def create_menu(self):
        menu = SelectStatusMenu()
        menu.status_selected.connect(self.setCurrentText)

        x = int(QCursor.pos().x() - menu.w / 2)
        y = int(QCursor.pos().y() - menu.h / 2)
        menu.exec(QPoint(x, y))
        

class SelectStatusMenu(QMenu):
    w: int = 120
    h: int = 120
    max_columns: int = 2

    colors = {
        "TODO": c.yellow,
        "WIP": c.orange,
        "WFA": c.purple,
        "DONE": c.green,
        "WAIT": c.text_white,
        "ERROR": c.red,
        "OMIT": c.light,
    }

    status_selected = Signal(str)

    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(1)

        self.setFixedSize(QSize(self.w, self.h))

        for i, (text, color) in enumerate(self.colors.items()):
            print(i, text, color)
            button = QPushButton(text)
            c_base = color.name()
            c_hover = color.lighter(110).name()
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            button.setStyleSheet(dedent("""
                QPushButton {
                    color: black ;
                    background-color:$c_base;
                    border: 3px solid transparent;
                }
                QPushButton:hover {
                    background-color:$c_hover;
                    border: none;
                }
                """)
                .replace("$c_base", c_base)
                .replace("$c_hover", c_hover))

            row = int(i / self.max_columns)
            column = i % self.max_columns
            button.clicked.connect(self.on_button_clicked)

            layout.addWidget(button, row, column)

    def on_button_clicked(self):
        button: QPushButton = self.sender()
        self.status_selected.emit(button.text())
        self.close()
