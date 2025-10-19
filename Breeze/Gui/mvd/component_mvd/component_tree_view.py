from PySide6.QtWidgets import QTreeView, QAbstractItemView

from Api.document_models.project_documents import Stage
from Gui.mvd.component_mvd.component_tree_item_delegate import ComponentTreeItemDelegate, ComponentVersionTreeItemDelegate
from Gui.mvd.component_mvd.component_tree_model import ComponentTreeModel, ComponentTreeItemRoles


# class AbstractTreeView(QTreeView):
#     @property
#     def selectedIndexes(self, /):


class ComponentTreeView(QTreeView):
    def __init__(self):
        super().__init__()
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self._model = ComponentTreeModel()
        self.setModel(self._model)

        self._item_delegate = ComponentTreeItemDelegate()
        self.setItemDelegateForColumn(0, self._item_delegate)

        self._version_item_delegate = ComponentVersionTreeItemDelegate()
        self.setItemDelegateForColumn(1, self._version_item_delegate)

        self.header().hide()
        self.expandAll()

        self._connect_signals()

    def refresh(self):
        self._model.refresh()  # activates expandAll() through a signal from the model

    def set_stage(self, stage: Stage):
        self._model.populate(stage=stage)
        self._item_delegate.set_stage(stage=stage)
        self.expandAll()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        index = self.indexAt(event.pos())
        if index.data(ComponentTreeItemRoles.version)  is None:
            self.edit(index)

    def _connect_signals(self):
        self._model.refreshed.connect(self.expandAll)
