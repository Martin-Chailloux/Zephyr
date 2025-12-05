from PySide6.QtWidgets import QAbstractItemView

from Api.document_models.project_documents import Stage, Version
from Gui.mvd.abstract_mvd import AbstractTreeView
from Gui.mvd.component_mvd.component_tree_item_delegate import ComponentTreeItemDelegate
from Gui.mvd.component_mvd.component_tree_model import (ComponentTreeModel, ComponentTreeItemRoles,
                                                        ComponentTreeItemMetrics)


class ComponentTreeView(AbstractTreeView):
    def __init__(self):
        super().__init__()
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self._model = ComponentTreeModel()
        self.setModel(self._model)

        self._item_delegate = ComponentTreeItemDelegate()
        self.setItemDelegateForColumn(0, self._item_delegate)

        self.header().hide()
        self.expandAll()

        self._connect_signals()

    def set_stage(self, stage: Stage):
        self._model.populate(stage=stage)
        self._item_delegate.set_stage(stage=stage)
        self.expandAll()

    def _set_hover_data(self, edit: bool=False):
        index = self._get_hovered_index()
        item = self._model.itemFromIndex(index)

        if index is None or item is None:
            return

        is_title: bool = index.data(ComponentTreeItemRoles.is_title)
        version: Version = index.data(ComponentTreeItemRoles.version)

        if is_title or version is None:
            item.setData(False, ComponentTreeItemRoles.can_edit_version_number)
            return

        mouse_position = self._get_mouse_pos()
        x, y, w, h = self._get_viewport_rect()

        can_edit_version_number = mouse_position.x() > w - ComponentTreeItemMetrics.version_width - ComponentTreeItemMetrics.edit_width
        item.setData(can_edit_version_number, ComponentTreeItemRoles.can_edit_version_number)

        # edit after a single click
        version = index.data(ComponentTreeItemRoles.version)
        if edit:
            if version is None or can_edit_version_number:
                self.edit(index)

    def refresh(self):
        # TODO: restore selection
        self._model.refresh()
        self.expandAll()
