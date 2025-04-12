from PySide6 import QtCore
from PySide6.QtCore import QModelIndex, QRect, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QImage, QBrush, QPainterPath
from PySide6.QtWidgets import QStyleOptionViewItem

from Data.studio_documents import User
from Gui.abstract_widgets.abstract_mvd import AbstractListDelegate
from Gui.stages_widgets.stage_list.stage_list_model import StageItemMetrics
from Gui.user_widgets.user_list.user_list_model import UserItemRoles


alignment = QtCore.Qt.AlignmentFlag


class UserListItemDelegate(AbstractListDelegate):
    def __init__(self):
        super().__init__()

    def _set_custom_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        self.user: User = index.data(UserItemRoles.user)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem , index: QModelIndex):
        self._set_data(option, index)

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.paint_selected_background(painter)
        self.paint_hover(painter)
        # self.paint_selected_underline(painter)
        self.paint_user(painter)

        self.paint_text(painter)

        painter.restore()

    def paint_user(self, painter: QPainter):
        margin = 2
        padding = 3
        x, y, w, h = self.get_item_rect()
        rect = QRect(x + padding, y+margin, h-2*margin, h-2*margin)

        image = QImage(self.user.icon_path)

        painter.save()

        # Set drawing data
        painter.setOpacity(self.opacity)
        painter.setBrush(QBrush(painter.background()))
        painter.setPen(QtCore.Qt.PenStyle.NoPen)

        # Set clip path
        path = QPainterPath(QPointF(x, y))
        path.addEllipse(rect)
        painter.setClipPath(path)

        # Draw image
        painter.drawImage(rect, image)

        painter.restore()

    def paint_text(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        color = QColor(self.palette.white_text)
        padding = 5

        painter.save()

        painter.setPen(QPen(color))
        painter.setOpacity(self.opacity + 0.3)

        font = painter.font()
        font.setBold(True)
        painter.setFont(font)
        rect = QRect(x + padding + h, y + h*1/8 - 1, w, h)
        painter.drawText(rect, self.user.pseudo, alignment.AlignTop | alignment.AlignLeft)

        font_size = painter.font().pointSizeF()
        font.setBold(False)
        font.setPointSizeF(font_size - 1.5)
        painter.setFont(font)

        painter.setOpacity(self.opacity)

        rect = QRect(x + padding + h, y + h/2, w, h/2)
        painter.drawText(rect, self.user.fullname, alignment.AlignTop | alignment.AlignLeft)
        painter.restore()
