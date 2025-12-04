from PySide6 import QtCore
from PySide6.QtCore import Signal, QItemSelectionModel, QItemSelection, QModelIndex

from Api.document_models.project_documents import Asset, Stage
from Gui.mvd.abstract_mvd import AbstractListView
from Gui.mvd.stage_mvd.stage_list_item_delegate import StageListItemDelegate, StageListItemDelegateMinimal
from Gui.mvd.stage_mvd.stage_list_model import StageListModel, StageItemRoles, StageListMinimalModel
from Gui.mvd.stage_mvd.stage_list_model import StageItemMetrics


class _StageListViewBase(AbstractListView):
    stage_selected = Signal()

    def __init__(self):
        super().__init__()
        self._set_model()
        self._set_delegate()

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
        super()._connect_signals()
        self.selectionModel().selectionChanged.connect(self._on_selection_changed)

    def _on_selection_changed(self):
        self.stage_selected.emit()


class StageListViewEditable(_StageListViewBase):
    def __init__(self):
        super().__init__()

    stage_data_modified = Signal()

    def _set_hover_data(self, edit: bool=False):
        self._model.clear_hover_data()

        index = self._get_hovered_index()
        item = self._model.itemFromIndex(index)

        if index is None or item is None:
            return

        mouse_position = self._get_mouse_pos()
        x, y, w, h = self._get_viewport_rect()
        status_x = w - StageItemMetrics.status_width
        user_x = status_x - StageItemMetrics.height

        can_edit_user = user_x < mouse_position.x() < status_x
        can_edit_status = status_x < mouse_position.x()
        item.setData(can_edit_user, StageItemRoles.can_edit_user)
        item.setData(can_edit_status, StageItemRoles.can_edit_status)

    def mousePressEvent(self, event):
        index = self._get_hovered_index()
        if index.data(StageItemRoles.can_edit_user) or index.data(StageItemRoles.can_edit_status):
            self.edit(index)
        else:
            super().mousePressEvent(event)


class StageListViewMinimal(_StageListViewBase):
    def _set_model(self):
        self._model = StageListMinimalModel()
        self.setModel(self._model)

    def _set_delegate(self):
        self._item_delegate = StageListItemDelegateMinimal()
        self.setItemDelegate(self._item_delegate)
