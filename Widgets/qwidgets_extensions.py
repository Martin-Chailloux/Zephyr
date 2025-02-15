import qtawesome
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QPushButton, QLabel, QWidget, QVBoxLayout, QTextEdit

from Gui.palette import Palette


class IconButton(QPushButton):
    palette: Palette = Palette.objects.get(name="dev")

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


class IconAsPixmap(QLabel):
    def __init__(self, icon_name: str, height: int = None):
        super().__init__()
        self.icon_name = icon_name
        if height is not None:
            self.setFixedHeight(height)

        icon = qtawesome.icon(self.icon_name)
        pixmap = icon.pixmap(self.sizeHint().height())
        self.setPixmap(pixmap)


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
