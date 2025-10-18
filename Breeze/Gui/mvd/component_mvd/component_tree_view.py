from PySide6.QtWidgets import QTreeView, QAbstractItemView

from Api.project_documents import Stage
from Gui.mvd.component_mvd.component_tree_item_delegate import ComponentTreeItemDelegate, ComponentVersionTreeItemDelegate
from Gui.mvd.component_mvd.component_tree_model import ComponentTreeModel, ComponentTreeItemRoles



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

    def set_stage(self, stage: Stage):
        self._model.populate(stage=stage)
        self._item_delegate.set_stage(stage=stage)
        self.expandAll()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        index = self.indexAt(event.pos())
        if index.data(ComponentTreeItemRoles.version)  is None:
            self.edit(index)


    # def set_components(self, components: list[Component]):
    #     self.blockSignals(True)
    #     self._model.populate(components=components)
    #     self.blockSignals(False)

    # def get_selected_component(self) -> Component | None:
    #     items = self.selected_items
    #     if not items:
    #         return None
    #     else:
    #         component: Component = items[0].data(ComponentTreeItemRoles.component)
    #         return component
