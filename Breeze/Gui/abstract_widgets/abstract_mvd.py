from PySide6.QtCore import QPoint, QModelIndex
from PySide6.QtGui import QCursor, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QListView


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
