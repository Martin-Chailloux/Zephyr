from dataclasses import dataclass

from PySide6.QtCore import Signal, QModelIndex, QItemSelectionModel

from Api.project_documents import Asset, Stage
from Gui.components.mvd.abstract_mvd import AbstractListView
from Gui.components.mvd.stage_mvd.stage_list_item_delegate import StageListItemDelegate, StageListMinimalItemDelegate
from Gui.components.mvd.stage_mvd.stage_list_model import StageListModel, StageItemRoles, StageListMinimalModel
from Gui.components.mvd.stage_mvd.stage_list_model import StageItemMetrics
from Gui.components.popups.status_select_popup import StatusSelectPopup
from Gui.components.popups.user_select_popup import UserSelectPopup


@dataclass
class StageListHoverData:
    index: QModelIndex = None
    on_user: bool = False
    on_status: bool = False


class _StageListBaseView(AbstractListView):
    stage_selected = Signal()

    def __init__(self):
        super().__init__()
        self._set_model()
        self._set_delegate()

        self.last_hover_data = StageListHoverData()
        self._connect_signals()

    def _set_model(self):
        self._model = StageListModel()
        self.setModel(self._model)

    def _set_delegate(self):
        self._item_delegate = StageListItemDelegate()
        self.setItemDelegate(self._item_delegate)

    def refresh(self):
        selected_indexes = self.selectionModel().selectedIndexes()
        self._model.refresh()

        if selected_indexes:
            index = self._model.index(selected_indexes[0].row(), 0)
            self.selectionModel().setCurrentIndex(index, QItemSelectionModel.SelectionFlag.Select)

    def set_asset(self, asset: Asset=None):
        if asset is None:
            return
        else:
            self.selectionModel().blockSignals(True)
            self._model.populate(stages=asset.stages)
            self.selectionModel().blockSignals(False)

    def set_stage(self, stage: Stage=None):
        if stage is None:
            return
        else:
            self.selectionModel().blockSignals(True)
            self._model.populate(stages=[stage])
            self.selectionModel().blockSignals(False)

    @property
    def stage(self) -> Stage | None:
        selected_indexes = self.selectionModel().selectedIndexes()
        if not selected_indexes:
            return None

        selected_index = selected_indexes[0]
        selected_item = self._model.item(selected_index.row())
        if selected_item is None:
            return None

        current_stage: Stage = selected_item.data(StageItemRoles.stage)
        return current_stage

    def select_stage(self, stage: Stage = None):
        if stage is None:
            self.selectionModel().clearSelection()
            return

        for row in range(self._model.rowCount()):
            index = self._model.index(row, 0)
            if stage == index.data(StageItemRoles.stage):
                self.select_row(row)

    def _connect_signals(self):
        self.selectionModel().selectionChanged.connect(self._on_selection_changed)

    def _on_selection_changed(self):
        self.stage_selected.emit()

    def _get_hovered_stage(self) -> Stage | None:
        hovered_item = self.get_hovered_item()
        if hovered_item is None:
            return None

        stage = hovered_item.data(StageItemRoles.stage)
        return stage


class StageListEditableView(_StageListBaseView):
    stage_data_modified = Signal()

    def refresh(self):
        super().refresh()
        self.set_items_hover_infos()
        self.viewport().update()

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
        hovered_item = self.get_hovered_item()
        if hovered_item is None:
            return

        # Set hovered components for the delegate
        hovered_item.setData(self.last_hover_data.on_user, StageItemRoles.user_is_hovered)
        hovered_item.setData(self.last_hover_data.on_status, StageItemRoles.status_is_hovered)

        # Set tooltip
        # TODO: pollutes the gui, use a help bar at the bottom of the app instead
        #  it receives text signals
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
            user_select_popup = UserSelectPopup(stage=self._get_hovered_stage())
            result = user_select_popup.show_menu(position=[0.5, 0.25])
            if result:
                self.stage_data_modified.emit()
                self.refresh()
        elif hover_data.on_status:
            status_select_popup = StatusSelectPopup(stage=self._get_hovered_stage())
            result = status_select_popup.show_menu(position=[0.5, 0.5])
            if result:
                self.stage_data_modified.emit()
                self.refresh()
        else:
            super().mousePressEvent(event)

    def leaveEvent(self, event):
        self._model.remove_items_hover()
        super().leaveEvent(event)


class StageListMinimalView(_StageListBaseView):
    def _set_model(self):
        self._model = StageListMinimalModel()
        self.setModel(self._model)

    def _set_delegate(self):
        self._item_delegate = StageListMinimalItemDelegate()
        self.setItemDelegate(self._item_delegate)
