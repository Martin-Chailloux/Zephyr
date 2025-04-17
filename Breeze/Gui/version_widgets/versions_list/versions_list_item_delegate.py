from wsgiref.simple_server import software_version

from PySide6 import QtCore
from PySide6.QtCore import QModelIndex, QRect
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QStyleOptionViewItem

from Data.project_documents import Version
from Gui.abstract_widgets.abstract_mvd import AbstractListDelegate
from Gui.version_widgets.versions_list.versions_list_model import VersionItemRoles

alignment = QtCore.Qt.AlignmentFlag


class VersionListItemDelegate(AbstractListDelegate):
    def __init__(self):
        super().__init__()

    def _set_custom_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        self.version: Version = index.data(VersionItemRoles.version)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem , index: QModelIndex):
        self._set_data(option, index)

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.paint_selected_background(painter)
        self.paint_hover(painter)
        self.paint_selected_underline(painter)
        self.paint_icon_circle(
            painter,
            path=self.version.last_user.icon_path
        )
        self.paint_version_num(painter)
        self.paint_software(painter)

        painter.restore()

    def paint_user(self, painter: QPainter):
        self.paint_icon_circle(
            painter,
            path=self.version.last_user.icon_path
        )

    def paint_version_num(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        padding = 2
        text = f"{self.version.number:03d}"

        painter.save()

        painter.setOpacity(self.opacity)
        rect = QRect(x + padding + h, y, w, h)
        painter.drawText(rect, text, alignment.AlignLeft | alignment.AlignVCenter)

        painter.restore()

    def paint_software(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        text_start: int = w - 36
        text = f".{self.version.software.extension}"

        painter.save()

        painter.setOpacity(self.opacity)
        self.paint_icon_circle(
            painter,
            path = self.version.software.icon_path,
            offset= text_start - h - 2,
        )
        rect = QRect(text_start, y, w, h)
        painter.drawText(rect, text, alignment.AlignLeft | alignment.AlignVCenter)

        painter.restore()
