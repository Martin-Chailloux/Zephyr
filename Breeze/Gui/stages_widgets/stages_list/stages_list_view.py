from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtCore import Signal, QPoint, QModelIndex
from PySide6.QtGui import QCursor, QStandardItem
from PySide6.QtWidgets import QListView

from Data.breeze_documents import Asset, Stage
from Gui.stages_widgets.stages_list.stages_list_item_delegate import StageListItemDelegate
from Gui.stages_widgets.stages_list.stages_list_model import StageListModel, StageItemRoles
from Gui.stages_widgets.stages_list.stages_list_model import StageListItemSizes
from Gui.status_widgets.status_subwidgets import SelectStatusMenu


@dataclass
class StageListHoverData:
    index: QModelIndex = None
    on_user: bool = False
    on_status: bool = False


class StageListView(QListView):
    stage_selected = Signal(str)

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

        self._model = StageListModel()
        self.setModel(self._model)

        self._item_delegate = StageListItemDelegate(widget=self)
        self.setItemDelegate(self._item_delegate)


        self.hover_data = StageListHoverData(index=self.get_hovered_index(),
                                             on_user=False,
                                             on_status=False)
        self._connect_signals()

    def set_asset(self, asset: Asset):
        self._model.set_asset(asset)

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

    def get_viewport_rect(self) -> (int, int, int, int):
        rect = self.viewport().rect()
        return rect.x(), rect.y(), rect.width(), rect.height()

    def _set_mouse_cursor(self):
        return
        # TODO: test alt: overlay an edit icon over the user
        if self.is_on_user or self.is_on_status:
            cursor_shape = QtCore.Qt.CursorShape.PointingHandCursor
        else:
            cursor_shape = QtCore.Qt.CursorShape.ArrowCursor
        cursor = QCursor()
        cursor.setShape(cursor_shape)
        self.setCursor(cursor)

    def get_hovered_index(self) -> QModelIndex:
        mouse_pos = self.get_mouse_pos()
        index = self.indexAt(mouse_pos)
        return index

    def get_hovered_item(self) -> QStandardItem:
        current_index = self.get_hovered_index()
        current_item = self._model.item(current_index.row())
        return current_item

    def mouseMoveEvent(self, event):
        x, y, w, h = self.get_viewport_rect()
        mouse_pos = self.get_mouse_pos()

        status_x = w - StageListItemSizes.status_w
        user_x = status_x - StageListItemSizes.height

        current_hover = StageListHoverData(index=self.get_hovered_index(),
                                           on_user=user_x < mouse_pos.x() < status_x,
                                           on_status=status_x < mouse_pos.x())

        if current_hover != self.hover_data:
            self._model.remove_items_hover()
            self.hover_data = current_hover
            self.set_items_hovered_parts()
            self.viewport().update()

        super().mouseMoveEvent(event)

    def set_items_hovered_parts(self):
        hovered_item = self.get_hovered_item()
        if hovered_item is None:
            return

        # Set hovered components for the delegate
        hovered_item.setData(self.hover_data.on_user, StageItemRoles.user_is_hovered)
        hovered_item.setData(self.hover_data.on_status, StageItemRoles.status_is_hovered)

        # Set tooltip
        # TODO: pollutes the gui, use a help bar at the bottom instead
        #  GOAL: global setting and shortcut to show / hide the help bars
        if hovered_item.data(StageItemRoles.user_is_hovered):
            tooltip = "Edit user"
        elif hovered_item.data(StageItemRoles.status_is_hovered):
            tooltip = "Edit status"
        else:
            tooltip = ""
        hovered_item.setToolTip(tooltip)

    def leaveEvent(self, event):
        self._model.remove_items_hover()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if self.hover_data.on_user:
            print("USER")

        elif self.hover_data.on_status:
            print("STATUS")
            menu = SelectStatusMenu()
            menu.exec()

        else:
            super().mousePressEvent(event)
