from operator import iconcat

import qtawesome
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton

from Gui.palette_api import ZPalette
from Widgets.qwidgets_extensions import ZIconButton

palette = ZPalette()


class ZSetFavoriteIconButton(ZIconButton):
    def __init__(self):
        super().__init__(icon_name="fa.star", width=24, icon_size=18, color=palette.text_white)
        self.unchecked_icon = qtawesome.icon("fa.star-o", color=self.color)

        self.setCheckable(True)
        self.clicked.connect(self.on_click)

        self.set_state(is_checked=False)  # TODO: from db

    def on_click(self, is_checked: bool):
        icon = self.icon if is_checked else self.unchecked_icon
        self.setIcon(icon)

    def set_state(self, is_checked: bool):
        self.setChecked(is_checked)
        self.on_click(is_checked=is_checked)
