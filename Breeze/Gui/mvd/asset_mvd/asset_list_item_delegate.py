import qtawesome
from PySide6 import QtCore
from PySide6.QtCore import QModelIndex, QRect
from PySide6.QtGui import QPainter, QPen, QBrush, QIcon
from PySide6.QtWidgets import QStyleOptionViewItem

from Api.breeze_app import BreezeApp
from Api.document_models.project_documents import Asset, SubUser
from Gui.mvd.abstract_mvd import AbstractItemDelegate
from Gui.mvd.asset_mvd.asset_list_model import AssetItemRoles, AssetItemMetrics

alignment = QtCore.Qt.AlignmentFlag


class AssetListItemDelegate(AbstractItemDelegate):
    def __init__(self):
        super().__init__()

    def _set_custom_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        self.asset: Asset = index.data(AssetItemRoles.asset)
        self.can_bookmark = index.data(AssetItemRoles.can_bookmark)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem , index: QModelIndex):
        self._set_data(option, index)

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        x, y, w, h = self.get_item_rect()

        self.paint_selected_background(painter)
        self.paint_hover(painter)

        self.paint_text(painter)
        self.paint_bookmark(painter, index)

        self.paint_selected_underline(painter)

        painter.restore()

    def paint_text(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        x += AssetItemMetrics.height

        painter.save()

        # asset path
        painter.setPen(QPen(BreezeApp.palette.white_text))
        rect = QRect(x, y, w, h)
        text = f"{self.asset.category} ⮞ {self.asset.name} ⮞ {self.asset.variant}"
        painter.drawText(rect, text, alignment.AlignLeft | alignment.AlignVCenter)

        painter.restore()

    def paint_bookmark(self, painter: QPainter, index: QModelIndex):
        x, y, w, h = self.get_item_rect()
        margin = 5 if self.can_bookmark else 7

        sub_user = SubUser.current()
        is_bookmarked = self.asset in sub_user.bookmarks
        icon_name = "fa.star" if is_bookmarked else "fa.star-o"

        icon_color = BreezeApp.palette.white_text

        painter.save()

        painter.setBrush(QBrush(icon_color))
        rect = QRect(x + margin, y + margin, AssetItemMetrics.height - 2 * margin, h - 2 * margin)
        icon: QIcon = qtawesome.icon(icon_name)
        icon.paint(painter, rect, QtCore.Qt.AlignmentFlag.AlignRight)

        painter.restore()