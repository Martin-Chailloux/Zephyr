from PySide6 import QtCore
from PySide6.QtCore import QModelIndex, QRect
from PySide6.QtGui import QPainter, QPen, QFontMetrics
from PySide6.QtWidgets import QStyleOptionViewItem

from Api.breeze_app import BreezeApp
from Api.project_documents import Component
from Gui.components.mvd.abstract_mvd import AbstractListDelegate
from Gui.components.mvd.component_mvd.component_list_model import ComponentItemRoles, ComponentItemMetrics

alignment = QtCore.Qt.AlignmentFlag


class ComponentListItemDelegate(AbstractListDelegate):
    def __init__(self):
        super().__init__()

    def _set_custom_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        self.component: Component = index.data(ComponentItemRoles.component)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem , index: QModelIndex):
        self._set_data(option, index)

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.paint_selected_background(painter)
        self.paint_hover(painter)
        self.paint_selected_underline(painter)

        self.paint_text(painter)

        painter.restore()

    def paint_text(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()

        painter.save()

        font_metrics = QFontMetrics(painter.font())

        # asset
        painter.setPen(QPen(BreezeApp.palette.white_text))
        asset = self.component.stage.asset
        text = f"{asset.category} ⮞ {asset.name} ⮞ {asset.variant} ⮞ "
        rect = QRect(x, y, w, h)
        painter.drawText(rect, text, alignment.AlignLeft | alignment.AlignVCenter)

        # stage
        x += font_metrics.horizontalAdvance(text)
        stage = self.component.stage
        painter.setPen(QPen(stage.stage_template.color))
        text = f"{stage.stage_template.label}"
        rect = QRect(x, y, w, h)
        painter.drawText(rect, text, alignment.AlignLeft | alignment.AlignVCenter)

        # component
        x += font_metrics.horizontalAdvance(text)
        painter.setOpacity(0.7)
        painter.setPen(QPen(BreezeApp.palette.white_text))
        text = f" ⮞ {self.component.label}"
        rect = QRect(x, y, w, h)
        painter.drawText(rect, text, alignment.AlignLeft | alignment.AlignVCenter)

        painter.restore()
