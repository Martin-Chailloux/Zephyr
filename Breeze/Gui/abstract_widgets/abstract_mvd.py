from PySide6.QtCore import QPoint, QModelIndex, QRect, QRectF
from PySide6.QtGui import QCursor, QStandardItem, QStandardItemModel, QPainter, QColor, QBrush, QPen
from PySide6.QtWidgets import QListView, QStyledItemDelegate, QStyleOptionViewItem, QStyle

from Data import app_dialog


class AbstractListView(QListView):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self._model: QStandardItemModel = None

    def _connect_signals(self):
        pass

    def _get_viewport_rect(self) -> (int, int, int, int):
        rect = self.viewport().rect()
        return rect.x(), rect.y(), rect.width(), rect.height()

    def _get_mouse_pos(self) -> QPoint:
        position: QPoint = self.mapFromGlobal(QCursor.pos())
        return position

    def _get_hovered_index(self) -> QModelIndex:
        mouse_pos = self._get_mouse_pos()
        index = self.indexAt(mouse_pos)
        return index

    def _get_hovered_item(self) -> QStandardItem:
        current_index = self._get_hovered_index()
        current_item = self._model.item(current_index.row())
        return current_item


class AbstractListModel(QStandardItemModel):
    def __init__(self):
        super().__init__()

    def add_item(self, **kwargs):
        pass

    @property
    def items(self):
        items = [self.item(row) for row in range(self.rowCount())]
        return items

    def refresh(self):
        return


class AbstractListDelegate(QStyledItemDelegate):
    palette = app_dialog.get_palette()

    def __init__(self):
        super().__init__()

    def _set_common_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        self.is_hovered = bool(option.state & QStyle.StateFlag.State_MouseOver)
        self.is_selected = bool(option.state & QStyle.StateFlag.State_Selected)
        self.item_rect: QRect = option.rect
        self.opacity: float = 1 if self.is_hovered or self.is_selected else 0.5

    def _set_custom_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        pass

    def _set_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        self._set_common_data(option, index)
        self._set_custom_data(option, index)

    def get_item_rect(self) -> (int, int, int, int):
        item_rect = self.item_rect
        return item_rect.x(), item_rect.y()+1, item_rect.width(), item_rect.height()-2

    def paint_hover(self, painter: QPainter):
        if not self.is_hovered:
            return

        x, y, w, h = self.get_item_rect()

        painter.save()
        color = QColor(self.palette.white_text)
        color.setAlphaF(0.1)
        painter.setPen(QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(color))
        painter.drawRect(QRectF(QRectF(x, y, w, h)))
        painter.restore()

    def paint_selected_background(self, painter: QPainter):
        if not self.is_selected:
            return

        x, y, w, h = self.get_item_rect()
        color = QColor(self.palette.white_text)
        color.setAlphaF(0.2)

        painter.save()

        painter.setPen(QPen(QColor(0, 0, 0, 0)))
        painter.setBrush(QBrush(color))
        painter.drawRect(x, y, w, h)

        painter.restore()

    def paint_selected_underline(self, painter: QPainter):
        if not self.is_selected:
            return

        x, y, w, h = self.get_item_rect()
        color = self.palette.green
        height = 2

        painter.save()

        painter.setPen(QPen(QColor(0, 0, 0, 0)))
        painter.setBrush(QBrush(color))
        painter.drawRect(QRectF(x, y+h-height, w, height))

        painter.restore()
