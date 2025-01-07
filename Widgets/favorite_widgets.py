import qtawesome
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton

from Gui.palette_api import ZPalette

palette = ZPalette()

class GSetFavoriteButton(QPushButton):
    # TODO: should be a generic widget
    # Separate uncheckable and checkable version
    unchecked_color = palette.medium
    unchecked_hover_color = palette.light

    def __init__(self, icon_name: str = None, size: int=None, checkable=False):
        super().__init__()
        self.checkable = checkable
        self.icon_name = icon_name or "fa.star"

        if checkable:
            self.setCheckable(True)
            self.checked_color = palette.text_white.darker(103)
            self.checked_hover_color = self.checked_color.lighter(120)
        else:
            self.checked_color = palette.medium
            self.checked_hover_color = palette.text_white

        self.update_icon(self.unchecked_color)
        self.clicked.connect(self.on_click)

        if size is not None:
            self.setFixedSize(QSize(size, size))

    def on_click(self, checked):
        color = self.checked_hover_color if checked else self.unchecked_hover_color
        self.update_icon(color)

    def enterEvent(self, event):
        if self.isChecked():
            self.update_icon(self.checked_hover_color)
        else:
            self.update_icon(self.unchecked_hover_color)

        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.isChecked():
            self.update_icon(self.checked_color)
        else:
            self.update_icon(self.unchecked_color)
        super().leaveEvent(event)

    def update_icon(self, color):
        self.setIcon(qtawesome.icon(self.icon_name, color=color))