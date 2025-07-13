from PySide6 import QtCore
from PySide6.QtCore import QModelIndex, QRect
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QStyleOptionViewItem

from Api.studio_documents import Software
from Gui.components.mvd.abstract_mvd import AbstractListDelegate
from Gui.components.mvd.software_mvd.software_list_model import SoftwareItemRoles

alignment = QtCore.Qt.AlignmentFlag


class SoftwareListItemDelegate(AbstractListDelegate):
    def __init__(self):
        super().__init__()

    def _set_custom_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        self.software: Software = index.data(SoftwareItemRoles.software)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem , index: QModelIndex):
        self._set_data(option, index)

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.paint_selected_background(painter)
        self.paint_hover(painter)
        self.paint_selected_underline(painter)
        self.paint_icon_circle(painter, icon_path=self.software.icon_path)

        self.paint_text(painter)

        painter.restore()

    def paint_text(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        color = QColor(self.palette.white_text)
        padding = 5

        painter.save()

        painter.setPen(QPen(color))
        painter.setOpacity(self.opacity)

        font = painter.font()
        font.setBold(True)
        painter.setFont(font)
        rect = QRect(x + padding + h, y, w, h)
        painter.drawText(rect, self.software.label, alignment.AlignLeft | alignment.AlignVCenter)
