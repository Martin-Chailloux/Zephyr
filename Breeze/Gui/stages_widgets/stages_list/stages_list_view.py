from dataclasses import dataclass

from PySide6.QtCore import Signal, QModelIndex

from Data.project_documents import Asset, Stage
from Dialogs.status_dialog import EditStatusMenu
from Gui.abstract_widgets.abstract_mvd import AbstractListView
from Gui.stages_widgets.stages_list.stages_list_item_delegate import StageListItemDelegate
from Gui.stages_widgets.stages_list.stages_list_model import StageListModel, StageItemRoles
from Gui.stages_widgets.stages_list.stages_list_model import StageListItemSizes


@dataclass
class StageListHoverData:
    index: QModelIndex = None
    on_user: bool = False
    on_status: bool = False
    stage: Stage = None


class StageListView(AbstractListView):
    stage_selected = Signal(str)

    def __init__(self):
        super().__init__()

        self._model = StageListModel()
        self.setModel(self._model)

        self._item_delegate = StageListItemDelegate(widget=self)
        self.setItemDelegate(self._item_delegate)

        self.last_hover_data = StageListHoverData()
        self._connect_signals()

    def set_asset(self, asset: Asset):
        self._model.set_asset(asset)
        if asset is None:
            self._model.clear()

    def _connect_signals(self):
        self.selectionModel().currentChanged.connect(self.on_selection_changed)

    def on_selection_changed(self):
        current_stage = self.get_selected_stage()
        if current_stage is None:
            return 
        self.stage_selected.emit(current_stage.longname)

    def get_selected_stage(self) -> Stage | None:
        current_item = self._model.item(self.currentIndex().row())
        if current_item is None:
            return None

        current_stage: Stage = current_item.data(StageItemRoles.stage)
        return current_stage

    def _get_hovered_stage(self) -> Stage | None:
        hovered_item = self._get_hovered_item()
        if hovered_item is None:
            return None

        stage = hovered_item.data(StageItemRoles.stage)
        return stage

    def _get_hover_data(self) -> StageListHoverData:
        x, y, w, h = self._get_viewport_rect()
        mouse_pos = self._get_mouse_pos()
        status_x = w - StageListItemSizes.status_w
        user_x = status_x - StageListItemSizes.height

        hover_data = StageListHoverData(index=self._get_hovered_index(),
                                           on_user=user_x < mouse_pos.x() < status_x,
                                           on_status=status_x < mouse_pos.x())
        return hover_data

    def set_items_hover_infos(self):
        hovered_item = self._get_hovered_item()
        if hovered_item is None:
            return

        # Set hovered components for the delegate
        hovered_item.setData(self.last_hover_data.on_user, StageItemRoles.user_is_hovered)
        hovered_item.setData(self.last_hover_data.on_status, StageItemRoles.status_is_hovered)

        # Set tooltip
        # TODO: pollutes the gui, use a help bar at the bottom of the app instead
        if hovered_item.data(StageItemRoles.user_is_hovered):
            tooltip = "Edit user"
        elif hovered_item.data(StageItemRoles.status_is_hovered):
            tooltip = "Edit status"
        else:
            tooltip = ""
        hovered_item.setToolTip(tooltip)

    def mouseMoveEvent(self, event):
        current_hover_data = self._get_hover_data()

        if current_hover_data != self.last_hover_data:
            self._model.remove_items_hover()
            self.last_hover_data = current_hover_data
            self.set_items_hover_infos()
            self.viewport().update()

        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if self.last_hover_data.on_user:
            pass
            # TODO
        elif self.last_hover_data.on_status:
            menu = EditStatusMenu(stage=self._get_hovered_stage())
            menu.exec()
            self.viewport().update()
        else:
            super().mousePressEvent(event)

    def leaveEvent(self, event):
        self._model.remove_items_hover()
        super().leaveEvent(event)
