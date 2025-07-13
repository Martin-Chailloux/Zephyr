from PySide6 import QtCore
from PySide6.QtCore import QModelIndex, QRect
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QStyleOptionViewItem

from Api.project_documents import Version
from Gui.components.mvd.abstract_mvd import AbstractListDelegate
from Gui.components.mvd.version_mvd.version_list_model import VersionItemRoles

alignment = QtCore.Qt.AlignmentFlag


class VersionListItemDelegate(AbstractListDelegate):
    datetime_width: int = 56
    num_width: int = 32

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

        # left
        self.paint_user(painter)
        self.paint_version_num(painter)

        # middle
        self.paint_comment(painter)

        # right
        x, y, w, h = self.get_item_rect()
        self.paint_time(painter, time=self.version.timestamp, rect=QRect(w - h - self.datetime_width, y, self.datetime_width, h))
        self.paint_software(painter)

        painter.restore()

    def paint_user(self, painter: QPainter):
        self.paint_icon_circle(
            painter,
            icon_path=self.version.last_user.icon_path,
        )

    def paint_version_num(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        text = f"{self.version.number:03d}"

        painter.save()

        painter.setOpacity(self.opacity)
        font = painter.font()
        font.setBold(True)
        painter.setFont(font)
        rect = QRect(x + h, y, self.num_width, h)
        painter.drawText(rect, text, alignment.AlignHCenter | alignment.AlignVCenter)

        painter.restore()

    def paint_software(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        margin: int = 4
        text = f".{self.version.software.extension}"
        x_offset = w - h

        painter.save()
        painter.setOpacity(self.opacity)

        # paint icon
        self.paint_icon_circle(
            painter,
            icon_path= self.version.software.icon_path,
            margin = margin,
            offset = [x_offset, - margin - 1, 0, 0],
        )

        # paint text
        font = painter.font()
        font.setPointSizeF(self.small_font_size)
        painter.setFont(font)
        rect = QRect(x_offset, y, h, h-1)
        painter.drawText(rect, text, alignment.AlignHCenter | alignment.AlignBottom)

        painter.restore()

    def paint_comment(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        text = self.version.comment
        start_x = x + h + self.num_width
        end_x = w - h - self.datetime_width - start_x
        margin = 8

        painter.save()
        painter.setOpacity(self.opacity)
        font = painter.font()
        font.setPointSizeF(self.medium_font_size)
        
        painter.setFont(font)
        rect = QRect(start_x + margin, y, end_x - margin, h)
        painter.drawText(rect, text, alignment.AlignLeft | alignment.AlignVCenter)

        painter.restore()
