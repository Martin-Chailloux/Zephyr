from PySide6.QtCore import Signal

from Api.document_models.project_documents import Component
from Gui.mvd.abstract_mvd import AbstractListView
from Gui.mvd.component_mvd.component_list_item_delegate import ComponentListItemDelegate
from Gui.mvd.component_mvd.component_list_model import ComponentItemRoles, ComponentListModel


class ComponentListView(AbstractListView):
    component_selected = Signal()

    def __init__(self):
        super().__init__()
        self._model = ComponentListModel()
        self.setModel(self._model.proxy)

        self._item_delegate = ComponentListItemDelegate()
        self.setItemDelegate(self._item_delegate)

        self.selectionModel().selectionChanged.connect(self.on_selection_changed)

    def set_components(self, components: list[Component]):
        self.blockSignals(True)
        self._model.populate(components=components)
        self.blockSignals(False)

    def get_selected_component(self) -> Component | None:
        items = self.selected_items
        if not items:
            return None
        else:
            component: Component = items[0].data(ComponentItemRoles.component)
            return component

    def set_text_filter(self, text: str):
        self._model.set_text_filter(text=text)

    def on_selection_changed(self):
        self.component_selected.emit()
