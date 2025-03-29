from dataclasses import dataclass

from PySide6.QtCore import Signal, QPoint
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QListView

from Data.breeze_documents import Asset
from Gui.stages_widgets.stages_list.stages_list_item_delegate import StageListItemDelegate
from Gui.stages_widgets.stages_list.stages_list_model import StageListModel
from Gui.stages_widgets.stages_list.stages_list_model import StageListItemSizes as dimensions

# TODO: recover edit stages button


class StageListView(QListView):
    stage_selected = Signal()

    def __init__(self):
        super().__init__()
        self._model = StageListModel()
        self._item_delegate = StageListItemDelegate(widget=self)

        self.setModel(self._model)
        self.setItemDelegate(self._item_delegate)

        self.setMouseTracking(True)
        self.last_mouse_x, self.last_mouse_y = self.get_mouse_position()


    def set_asset(self, asset: Asset):
        self._model.set_asset(asset)

    def get_mouse_position(self) -> (int, int):
        position: QPoint = self.mapFromGlobal(QCursor.pos())
        return position.x(), position.y()

    def get_viewport_rect(self) -> (int, int, int, int):
        rect = self.viewport().rect()
        return rect.x(), rect.y(), rect.width(), rect.height()

    def mouseMoveEvent(self, event):
        # optim: only update when needed
        x, y, w, h = self.get_viewport_rect()
        mouse_x, mouse_y = self.get_mouse_position()

        status_x = w - dimensions.status_w
        user_x = status_x - dimensions.height

        # crossed item
        if int(mouse_y / dimensions.height) != int(self.last_mouse_y / dimensions.height):
            print(f"CROSSED ITEM")
            self.viewport().update()

        # crossed user
        elif self.last_mouse_x >= user_x >= mouse_x or self.last_mouse_x <= user_x <= mouse_x:
            print(f"CROSSED USER")
            self.viewport().update()

        # crossed status
        elif self.last_mouse_x >= status_x >= mouse_x or self.last_mouse_x <= user_x <= mouse_x:
            print(f"CROSSED STATUS")
            self.viewport().update()

        super().mouseMoveEvent(event)

        self.last_mouse_x = mouse_x
        self.last_mouse_y = mouse_y
