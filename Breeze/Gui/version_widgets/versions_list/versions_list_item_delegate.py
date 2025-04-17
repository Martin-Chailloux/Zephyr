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
        self.paint_text(painter)

        painter.restore()

    def paint_text(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        color = QColor(self.palette.white_text)
        padding = 2
        text = f"{self.version.number:03d}.{self.version.extension}"
        text = f"{self.version.number:03d}"

        painter.save()

        painter.setPen(QPen(color))
        painter.setOpacity(self.opacity)

        font = painter.font()
        painter.setFont(font)
        rect = QRect(x + padding + h, y, w, h)
        painter.drawText(rect, text, alignment.AlignLeft | alignment.AlignVCenter)

    def paint_user(self, painter: QPainter):
        self.paint_icon_circle(
            painter,
            path=self.version.last_user.icon_path
        )

    def paint_software(self):
        pass
        # TODO: replace version.extension with version.software