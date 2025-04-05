from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtCore import Signal, QPoint
from PySide6.QtGui import QCursor, QStandardItem
from PySide6.QtWidgets import QListView

from Data.breeze_documents import Asset, Stage
from Gui.stages_widgets.stages_list.stages_list_item_delegate import StageListItemDelegate
from Gui.stages_widgets.stages_list.stages_list_model import StageListModel, StageItemRoles
from Gui.stages_widgets.stages_list.stages_list_model import StageListItemSizes as dimensions

# TODO: recover edit stages button


class StageListView(QListView):
    stage_selected = Signal(str)

    def __init__(self):
        super().__init__()
        self._model = StageListModel()
        self._item_delegate = StageListItemDelegate(widget=self)

        self.setModel(self._model)
        self.setItemDelegate(self._item_delegate)

        self.setMouseTracking(True)
        self.last_mouse_pos = self.get_mouse_pos()
        self.last_hovered_item_index: int = self.get_hovered_item_index()

        self.is_on_user: bool = False
        self.is_on_status: bool = False

        self._connect_signals()

    def set_asset(self, asset: Asset):
        self._model.set_asset(asset)

    # def refresh(self):
    #     self._model.set_asset(asset=self._model.asset)

    def _connect_signals(self):
        self.selectionModel().currentChanged.connect(self.on_selection_changed)

    def on_selection_changed(self):
        current_item = self._model.item(self.currentIndex().row())
        if current_item is None:
            return
        current_stage: Stage = current_item.data(StageItemRoles.stage)
        self.stage_selected.emit(current_stage.longname)

    def get_mouse_pos(self) -> QPoint:
        position: QPoint = self.mapFromGlobal(QCursor.pos())
        return position

    def get_hovered_item_index(self) -> int:
        mouse_position = self.get_mouse_pos()
        return int(mouse_position.y() / dimensions.height)

    def get_viewport_rect(self) -> (int, int, int, int):
        rect = self.viewport().rect()
        return rect.x(), rect.y(), rect.width(), rect.height()

    def _set_mouse_cursor(self):
        # TODO: test alt: overlay an edit icon over the user
        if self.is_on_user or self.is_on_status:
            cursor_shape = QtCore.Qt.CursorShape.PointingHandCursor
        else:
            cursor_shape = QtCore.Qt.CursorShape.ArrowCursor
        cursor = QCursor()
        cursor.setShape(cursor_shape)
        self.setCursor(cursor)

    def get_hovered_item(self) -> QStandardItem:
        current_index = self.indexAt(self.get_mouse_pos())
        current_item = self._model.item(current_index.row())
        return current_item

    def mouseMoveEvent(self, event):
        # TODO: update the delegate from here using the item index (from self.get_hovered_item_index())
        #  <- bug: it does not work when moving very slowy
        #  + the delegate should not be responsible for logic anyway
        # optim: only update when needed
        x, y, w, h = self.get_viewport_rect()
        mouse_pos = self.get_mouse_pos()

        status_x = w - dimensions.status_w
        user_x = status_x - dimensions.height

        needs_update: bool = False

        # crossed item
        if self.get_hovered_item_index() != self.last_hovered_item_index:
            needs_update = True

        # crossed user
        elif self.last_mouse_pos.x() >= user_x >= mouse_pos.x() or self.last_mouse_pos.x() <= user_x <= mouse_pos.x():
            needs_update = True

        # crossed status
        elif self.last_mouse_pos.x() >= status_x >= mouse_pos.x() or self.last_mouse_pos.x() <= status_x <= mouse_pos.x():
            needs_update = True

        if needs_update:
            self.is_on_user = user_x < mouse_pos.x() < status_x
            self.is_on_status = status_x < mouse_pos.x()

            self._model.remove_items_hover()
            self.set_hovered_items()

            self._set_mouse_cursor()
            self.viewport().update()

        super().mouseMoveEvent(event)
        self.last_mouse_pos = mouse_pos
        self.last_hovered_item_index = self.get_hovered_item_index()

    def set_hovered_items(self):
        hovered_item = self.get_hovered_item()
        if hovered_item is not None:
            hovered_item.setData(self.is_on_user, StageItemRoles.user_is_hovered)
            hovered_item.setData(self.is_on_status, StageItemRoles.status_is_hovered)

    def leaveEvent(self, event):
        self._model.remove_items_hover()
        super().leaveEvent(event)

    def enterEvent(self, event):
        self.set_hovered_items()
        super().enterEvent(event)