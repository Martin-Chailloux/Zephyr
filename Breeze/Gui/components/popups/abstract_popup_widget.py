from PySide6 import QtCore
from PySide6.QtCore import QPoint
from PySide6.QtGui import QCursor, QMouseEvent
from PySide6.QtWidgets import QDialog


class AbstractPopupWidget(QDialog):
    def __init__(self, w: int, h: int, show_borders: bool=False,
                 position: list[float] = None):
        super().__init__()
        self.w = w
        self.h = h
        self.position = position or [0, 0]

        if not show_borders:
            self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        if w is not None:
            self.setFixedWidth(w)
        if h is not None:
            self.setFixedHeight(h)

    def exec(self):
        x = int(QCursor.pos().x())
        y = int(QCursor.pos().y())

        x -= self.w * self.position[0]
        y -= self.h * self.position[1]

        self.move(QPoint(x, y))

        return super().exec()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if isinstance(event, QMouseEvent):
            if event.button() == QtCore.Qt.MouseButton.RightButton:
                self.reject()
