import qtawesome
from PySide6.QtCore import QSize
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QPushButton, QLabel

from Gui.palette import Palette


class ZIconButton(QPushButton):
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

# TODO: full transparancy + color shift
class ZTransparentIconButton0(ZIconButton):
    def __init__(self, icon_name: str, width: int, icon_size=None, color: str = "white", alpha: int = 30):
        super().__init__(icon_name, width, icon_size, color)
        color = QColor(color)
        color.setAlpha(alpha)
        hexa = color.name(format=QColor.NameFormat.HexArgb)
        self.setStyleSheet(f"background-color: {hexa}")


class ZTransparentIconButton(ZIconButton):
    def __init__(self, icon_name: str, width: int, icon_size=None, color: str = "white", alpha: int=90):
        super().__init__(icon_name, width, icon_size, color)
        hexa = QColor(self.color)
        hexa.setAlpha(alpha)
        hexa = hexa.name(format=QColor.NameFormat.HexArgb)
        self.setStyleSheet(f"background-color: transparent")

        self.icon_transparent = qtawesome.icon(icon_name, color=hexa)
        self.clicked.connect(self.on_click)
        self.on_click()

    def on_click(self):
        self.setIcon(self.icon_transparent)

    def enterEvent(self, event):
        self.setIcon(self.icon)

    def leaveEvent(self, event):
        self.setIcon(self.icon_transparent)


class ZImage(QLabel):
    def __init__(self, icon_name: str, height: int = None):
        super().__init__()
        self.icon_name = icon_name
        if height is not None:
            self.setFixedHeight(height)

        icon = qtawesome.icon(self.icon_name)
        pixmap = icon.pixmap(self.sizeHint().height())
        self.setPixmap(pixmap)
