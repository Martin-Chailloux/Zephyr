import qtawesome
from PySide6 import QtCore
from PySide6.QtCore import QSize, QPoint
from PySide6.QtGui import QCursor, QIcon
from PySide6.QtWidgets import QPushButton, QLabel, QWidget, QVBoxLayout, QTextEdit, QDialog

from Data import app_dialog
from Data.studio_documents import Palette


class IconButton(QPushButton):
    palette = app_dialog.get_palette()

    def __init__(self, icon_name: str, width: int = 30, icon_size: int=20, color: str = "white"):
        super().__init__()

        self.setFixedSize(QSize(width, width))
        color = color or self.palette.white_text
        icon = qtawesome.icon(icon_name, color=color)
        self.setIcon(icon)
        self.setIconSize(QSize(icon_size, icon_size))

        # public vars
        self.color = color
        self.icon = icon


class IconLabel(QLabel):
    def __init__(self, icon: QIcon, height: int = None):
        super().__init__()
        if height is not None:
            self.setFixedHeight(height)

        height = self.sizeHint().height()

        pixmap = icon.pixmap(height - int(height/8))  # A full size icon is too big to fit in
        self.setPixmap(pixmap)

        self.setFixedSize(QSize(height, height))


class TextBox(QWidget):
    def __init__(self, title: str):
        super().__init__()
        self.title = title

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(self.title)
        layout.addWidget(label)

        text_edit = QTextEdit()
        layout.addWidget(text_edit)

        # public vars
        self.text_edit = text_edit


class PushButtonAutoWidth(QPushButton):
    def __init__(self, text: str=None, icon_name: str=None, tooltip: str=None,
                 height: int=28, fixed_width: bool=False):
        super().__init__()
        if text is not None:
            self.setText(text)
        if icon_name is not None:
            self.setIcon(qtawesome.icon(icon_name))
        if tooltip is not None:
            self.setToolTip(tooltip)

        self.setFixedHeight(height)
        width = self.sizeHint().width() + 12
        self.setFixedWidth(width) if fixed_width else self.setMinimumWidth(width)
