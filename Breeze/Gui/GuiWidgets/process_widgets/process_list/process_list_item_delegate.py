from PySide6 import QtCore
from PySide6.QtCore import QModelIndex, QRect
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QStyleOptionViewItem

from Data.studio_documents import User, Process
from Gui.GuiWidgets.abstract_widgets.abstract_mvd import AbstractListDelegate
from Gui.GuiWidgets.process_widgets.process_list.process_list_model import ProcessItemRoles
from Gui.GuiWidgets.user_widgets.user_list.user_list_model import UserItemRoles


alignment = QtCore.Qt.AlignmentFlag


class ProcessListItemDelegate(AbstractListDelegate):
    def __init__(self):
        super().__init__()

    def _set_custom_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        self.process: Process = index.data(ProcessItemRoles.process)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem , index: QModelIndex):
        self._set_data(option, index)
        # TODO: paint icon

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.paint_selected_background(painter)
        self.paint_hover(painter)
        self.paint_selected_underline(painter)
        # self.paint_icon_circle(painter, icon_path=self.user.icon_path)
        self.paint_text(painter)

        painter.restore()

    def paint_text(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        color = QColor(self.palette.white_text)
        padding = 5

        painter.save()

        painter.setPen(QPen(color))

        font = painter.font()
        painter.setFont(font)
        rect = QRect(x, y, w, h)
        painter.drawText(rect, self.process.label, alignment.AlignVCenter | alignment.AlignLeft)
