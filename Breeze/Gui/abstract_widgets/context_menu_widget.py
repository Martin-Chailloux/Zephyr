from PySide6 import QtCore
from PySide6.QtCore import QSize, QPoint
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QDialog


class ContextMenuWidget(QDialog):
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
