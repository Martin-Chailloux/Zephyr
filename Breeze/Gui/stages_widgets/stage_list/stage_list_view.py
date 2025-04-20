from dataclasses import dataclass

from PySide6.QtCore import Signal, QModelIndex, QItemSelectionModel

from Data.project_documents import Asset, Stage
from Gui.abstract_widgets.abstract_mvd import AbstractListView
from Gui.stages_widgets.stage_list.stage_list_item_delegate import StageListItemDelegate
from Gui.stages_widgets.stage_list.stage_list_model import StageListModel, StageItemRoles
from Gui.stages_widgets.stage_list.stage_list_model import StageItemMetrics
from Gui.status_widgets.status_select_menu import StatusSelectMenu
from Gui.user_widgets.user_select_menu import UserSelectMenu


@dataclass
class StageListHoverData:
    index: QModelIndex = None
    on_user: bool = False
    on_status: bool = False


class StageListView(AbstractListView):
    stage_selected = Signal(str)
    stage_data_modified = Signal()

    def __init__(self):
        super().__init__()

        self._model = StageListModel()
        self.setModel(self._model)

        self._item_delegate = StageListItemDelegate()
        self.setItemDelegate(self._item_delegate)

        self.last_hover_data = StageListHoverData()
        self._connect_signals()

    def refresh(self):
        # TODO: quand y en a qu'un ça refresh pas
        selected_indexes = self.selectionModel().selectedIndexes()
        self._model.refresh()
        if selected_indexes:
            index = self._model.index(selected_indexes[0].row(), 0)
            self.selectionModel().setCurrentIndex(index, QItemSelectionModel.SelectionFlag.Select)
        self.set_items_hover_infos()
        self.viewport().update()

    def set_asset(self, asset: Asset):
        self._model.set_asset(asset)

    def set_stage(self, stage: Stage):
        self._model.clear()
        if stage is not None:
            self._model.add_item(stage=stage)

    def _connect_signals(self):
        self.selectionModel().selectionChanged.connect(self.on_selection_changed)

    def on_selection_changed(self):
        current_stage = self.get_selected_stage()
        if current_stage is None:
            self.stage_selected.emit("")
            return
        self.stage_selected.emit(current_stage.longname)

    def get_selected_stage(self) -> Stage | None:
        selected_indexes = self.selectionModel().selectedIndexes()
        if not selected_indexes:
            return None
        selected_index = selected_indexes[0]
        selected_item = self._model.item(selected_index.row())
        if selected_item is None:
            return None

        current_stage: Stage = selected_item.data(StageItemRoles.stage)
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
        status_x = w - StageItemMetrics.status_w
        user_x = status_x - StageItemMetrics.height

        index = self._get_hovered_index()
        on_user = index.row() != -1 and user_x < mouse_pos.x() < status_x
        on_status = index.row() != -1 and status_x < mouse_pos.x()
        hover_data = StageListHoverData(index=index,
                                        on_user=on_user,
                                        on_status=on_status)
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
        hover_data = self._get_hover_data()
        if hover_data.on_user:
            menu = UserSelectMenu(stage=self._get_hovered_stage())
            menu.exec()
            self.stage_data_modified.emit()
            self.refresh()
        elif hover_data.on_status:
            menu = StatusSelectMenu(stage=self._get_hovered_stage())
            menu.exec()
            self.stage_data_modified.emit()
            self.refresh()
        else:
            super().mousePressEvent(event)

    def leaveEvent(self, event):
        self._model.remove_items_hover()
        super().leaveEvent(event)
