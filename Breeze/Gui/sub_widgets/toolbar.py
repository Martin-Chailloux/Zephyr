from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QPushButton

from Utils.sub_widgets import IconButton


class ToolBar(QWidget):
    # TODO: move to some utils generic folder
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._init_ui()

    def _init_ui(self):
        pass

    def add_divider(self) -> QFrame:
        # TODO: the stylesheet removes the line
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Plain)
        divider.setFixedHeight(12)
        self.layout().addWidget(divider)
        return divider

    def add_button(self, icon_name: str, tooltip: str) -> QPushButton:
        button = IconButton(icon_name=icon_name, wh=28, icon_size=24)
        button.setToolTip(tooltip)
        self.layout().addWidget(button)
        return button
