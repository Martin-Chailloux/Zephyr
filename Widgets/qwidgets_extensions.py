import qtawesome
from PySide6 import QtCore
from PySide6.QtCore import QSize, Signal, QPoint
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QPushButton, QLabel, QWidget, QVBoxLayout, QTextEdit, QDialog

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


class ContextWidget(QDialog):
    def __init__(self, w: int, h: int,
                 align_h: QtCore.Qt.AlignmentFlag=QtCore.Qt.AlignmentFlag.AlignLeft,
                 align_v: QtCore.Qt.AlignmentFlag=QtCore.Qt.AlignmentFlag.AlignTop):
        super().__init__()
        self.w = w
        self.h = h
        self.align_h = align_h
        self.align_v = align_v

        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(QSize(w, h))

    def exec(self):
        x = int(QCursor.pos().x())
        y = int(QCursor.pos().y())

        if self.align_h in [QtCore.Qt.AlignmentFlag.AlignCenter, QtCore.Qt.AlignmentFlag.AlignHCenter]:
            x -= self.w / 2
        elif self.align_h in [QtCore.Qt.AlignmentFlag.AlignRight]:
            x -= self.w

        if self.align_v in [QtCore.Qt.AlignmentFlag.AlignCenter, QtCore.Qt.AlignmentFlag.AlignVCenter]:
            y -= self.h / 2
        elif self.align_v in [QtCore.Qt.AlignmentFlag.AlignBottom]:
            y -= self.h

        self.move(QPoint(x, y))
        super().exec()