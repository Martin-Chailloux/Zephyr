from PySide6 import QtCore
from PySide6.QtCore import QModelIndex
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem

from Breeze.Gui.version_widgets.versions_list.versions_list_model import VersionItemRoles


# TODO: comment, date, hour, user
#  in infos:
#   - creation date / hour / user
#   - current date / hour / user
#   - todo list
#   - complete comment
#   - time spent
#   - software

class VersionsListItemDelegate(QStyledItemDelegate):
    def __init__(self):
        super().__init__()

    def paint(self, painter: QPainter, option: QStyleOptionViewItem , index: QModelIndex):
        super().paint(painter, option, index)

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        item_rect = option.rect
        af = QtCore.Qt.AlignmentFlag

        number = f"   {index.data(VersionItemRoles.number):03d}"
        painter.drawText(item_rect, number, af.AlignVCenter | af.AlignLeft)

        name = index.data(VersionItemRoles.name)
        painter.drawText(item_rect, name, af.AlignVCenter | af.AlignCenter)

        painter.restore()