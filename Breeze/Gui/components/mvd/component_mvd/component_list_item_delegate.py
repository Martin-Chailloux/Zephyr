from PySide6 import QtCore
from PySide6.QtCore import QModelIndex, QRect
from PySide6.QtGui import QPainter, QPen, QFontMetrics
from PySide6.QtWidgets import QStyleOptionViewItem

from Api.breeze_app import BreezeApp
from Api.project_documents import Component
from Gui.components.mvd.abstract_mvd import AbstractItemDelegate
from Gui.components.mvd.component_mvd.component_list_model import ComponentItemRoles, ComponentItemMetrics

alignment = QtCore.Qt.AlignmentFlag


class ComponentListItemDelegate(AbstractItemDelegate):
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

        self.paint_component(painter, component=self.component)

        painter.restore()
