import qtawesome
from PySide6 import QtCore
from PySide6.QtCore import QModelIndex, QRect, QRectF
from PySide6.QtGui import QPainter, QBrush, QColor, QPen, QIcon
from PySide6.QtWidgets import QStyleOptionViewItem

from Api.breeze_app import BreezeApp
from Api.studio_documents import StageTemplate
from Gui.components.mvd.abstract_mvd import AbstractListDelegate
from Gui.components.mvd.stage_mvd.stage_list_model import StageItemMetrics
from Gui.components.mvd.stage_template_mvd.stage_template_list_model import StageTemplateItemRoles

alignment = QtCore.Qt.AlignmentFlag


class StageTemplateListItemDelegate(AbstractListDelegate):
    def __init__(self):
        super().__init__()

    def _set_custom_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        self.stage_template: StageTemplate = index.data(StageTemplateItemRoles.stage_template)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem , index: QModelIndex):
        self._set_data(option, index)

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.paint_selected_background(painter)
        self.paint_hover(painter)

        self.paint_logo(painter)
        self.paint_text(painter)

        self.paint_selected_underline(painter)

        painter.restore()

    def paint_logo(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        margin = 3 if self.is_hovered or self.is_selected else 5

        background_color = self.stage_template.color
        icon_color = BreezeApp.palette.white_text

        painter.save()

        painter.setOpacity(self.opacity)
        painter.setPen(QColor(0, 0, 0, 0))
        rect = QRectF(x, y, StageItemMetrics.logo_w, h)
        painter.setBrush(QBrush(background_color))
        painter.drawRect(rect)

        painter.setBrush(QBrush(icon_color))
        rect = QRect(x + margin, y + margin, StageItemMetrics.logo_w - 2 * margin, h - 2 * margin)
        icon: QIcon = qtawesome.icon(self.stage_template.icon_name, opacity=self.opacity)
        icon.paint(painter, rect, QtCore.Qt.AlignmentFlag.AlignRight)

        painter.restore()

    def paint_text(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        color = QColor(BreezeApp.palette.white_text)
        padding = 12

        painter.save()
        painter.setOpacity(self.opacity)
        painter.setPen(QPen(color))
        rect = QRect(x + padding + StageItemMetrics.logo_w, y, w, h)
        painter.drawText(rect, self.stage_template.label, alignment.AlignVCenter | alignment.AlignLeft)
        painter.restore()
