import qtawesome
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QLabel, QWidget, QVBoxLayout, QTextEdit

from Api.breeze_app import BreezeApp


class IconButton(QPushButton):
    palette = BreezeApp.palette

    def __init__(self, icon_name: str, width: int = 28, icon_size: int=18, color: str = "white"):
        super().__init__()

        self.setFixedSize(QSize(width, width))
        color = color or BreezeApp.palette.white_text
        icon = qtawesome.icon(icon_name, color=color)
        self.setIcon(icon)
        self.setIconSize(QSize(icon_size, icon_size))

        # public vars
        self.color = color
        self.icon = icon


class IconLabel(QLabel):
    def __init__(self, icon: QIcon, wh: int = 24):
        super().__init__()

        icon = qtawesome.icon(icon)
        pixmap = icon.pixmap(wh - 2)
        self.setPixmap(pixmap)

        self.setFixedSize(QSize(wh, wh))


class TextBox(QWidget):
    def __init__(self, title: str=None):
        super().__init__()
        self.title = title

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        if self.title is not None:
            label = QLabel(self.title)
            layout.addWidget(label)
            font = label.font()
            font.setBold(True)
            label.setFont(font)

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
