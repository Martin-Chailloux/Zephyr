import qtawesome
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QPushButton, QLabel

from Gui.palette_api import ZPalette

palette = ZPalette()


class ZIconButton(QPushButton):
    def __init__(self, icon_name: str, width: int, icon_size=None, icon_color: str = "white"):
        super().__init__()
        icon_size = icon_size or width

        self.setFixedSize(QSize(width, width))
        color = icon_color or palette.text_white
        icon = qtawesome.icon(icon_name, color=color)
        self.setIcon(icon)
        self.setIconSize(QSize(icon_size, icon_size))


class ZImage(QLabel):
    def __init__(self, icon_name: str, height: int = None):
        super().__init__()
        self.icon_name = icon_name
        if height is not None:
            self.setFixedHeight(height)

        icon = qtawesome.icon(self.icon_name)
        pixmap = icon.pixmap(self.sizeHint().height())
        self.setPixmap(pixmap)
