import qtawesome
from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel

from Widgets.qt_extensions import ZImage


class ZHeader(QWidget):
    def __init__(self, text, icon_name: str = None, height: int = 18):
        super().__init__()
        self.text = text
        self.icon_name = icon_name
        self.h = height

        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)

        if self.icon_name is not None:
            image = ZImage(icon_name=self.icon_name, height=self.h*2)
            layout.addWidget(image)

        label = QLabel(self.text)
        layout.addWidget(label)
        label.setStyleSheet(f"font: {self.h}pt 'Montserrat semibold'")

