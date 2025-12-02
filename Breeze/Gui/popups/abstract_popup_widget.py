from PySide6 import QtCore
from PySide6.QtCore import QPoint
from PySide6.QtGui import QCursor, QMouseEvent
from PySide6.QtWidgets import QDialog


class AbstractPopupWidget(QDialog):
    def __init__(self, w: int = None, h: int = None, show_borders: bool=False):
        super().__init__()
        self.w = w
        self.h = h

        if not show_borders:
            self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        if w is not None:
            self.setFixedWidth(w)
        if h is not None:
            self.setFixedHeight(h)

    def show_menu(self, position: list[float] = None) -> int:
        """
        :param position: [x, y]: range 0 -> 1, equals to [min_w -> max_w, min_h -> max_h]
        :return: [int]: 0 == reject ; 1 == accept ; 2, 3, etc. == custom inputs
        """
        # get mouse position
        x = int(QCursor.pos().x())
        y = int(QCursor.pos().y())

        # offset the menu
        position = position or [0, 0]
        x -= self.sizeHint().width() * position[0]
        y -= self.sizeHint().height() * position[1]
        self.move(QPoint(x, y))

        # show the menu
        return self.exec()

    def mousePressEvent(self, event):
        if not isinstance(event, QMouseEvent):
            raise NotImplementedError("DEV: Not a mouse event")

        match event.button():
            case QtCore.Qt.MouseButton.RightButton:
                self.reject()
            case _:
                super().mousePressEvent(event)
