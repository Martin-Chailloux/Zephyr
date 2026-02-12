from PySide6 import QtCore
from PySide6.QtCore import QSize, QPointF, Signal, QRect
from PySide6.QtGui import QPaintEvent, QPainter, QImage, QBrush, QPainterPath, QMouseEvent, QEnterEvent
from PySide6.QtWidgets import QLabel

from Api.document_models.studio_documents import User


class UserPicture(QLabel):
    clicked = Signal()

    def __init__(self, user: User = None, wh: int=48, clickable: bool=False):
        super().__init__('User not found')
        self.user = user
        self.clickable = clickable
        self.setFixedSize(QSize(wh, wh))

    def set_user(self, user: User):
        self.user = user

    def paintEvent(self, event: QPaintEvent):
        if self.user is None:
            super().paintEvent(event)
            return

        painter = QPainter(self)
        rect = event.rect()

        image = QImage(self.user.icon_path)
        painter.setBrush(QBrush(painter.background()))
        painter.setPen(QtCore.Qt.PenStyle.NoPen)

        # Set clip path
        icon_path = QPainterPath(QPointF(rect.x(), rect.y()))
        icon_path.addEllipse(rect)
        painter.setClipPath(icon_path)

        # Draw image
        painter.drawImage(rect, image)

    def mousePressEvent(self, event: QMouseEvent):
        if self.clickable:
            match event.button():
                case QtCore.Qt.MouseButton.LeftButton:
                    print(f"PRESS")
                case _:
                    print("ignore")

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.clickable:
            match event.button():
                case QtCore.Qt.MouseButton.LeftButton:
                    print(f"RELEASE")
                case _:
                    print("ignore")

        super().mouseReleaseEvent(event)

    def enterEvent(self, event: QEnterEvent):
        print(f"ENTER")
        super().enterEvent(event)

    def leaveEvent(self, event: QEnterEvent):
        print(f"LEAVE")
        super().leaveEvent(event)
