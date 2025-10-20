from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtCore import QSize, QSortFilterProxyModel, QModelIndex
from PySide6.QtGui import QStandardItem

from Api.document_models.project_documents import Component
from Gui.mvd.abstract_mvd import AbstractItemModel


@dataclass
class ComponentItemRoles:
    component = QtCore.Qt.ItemDataRole.UserRole


@dataclass
class ComponentItemMetrics:
    height: int = 36
    stage_w: int = 64


class ComponentListModel(AbstractItemModel):
    def __init__(self):
        super().__init__()
        self.components: list[Component] = []
        self.filtered_components: list[Component] = []
        self.proxy = ComponentListProxyModel()
        self.proxy.setSourceModel(self)

    def add_item(self, component: Component):
        row = self.rowCount()

        item = QStandardItem()
        item.setSizeHint(QSize(0, ComponentItemMetrics.height))
        item.setEditable(False)

        item.setData(component, ComponentItemRoles.component)
        item.setData(component.longname.lower(), QtCore.Qt.ItemDataRole.DisplayRole)  # used for filtering

        self.setItem(row, item)
        self.components.append(component)

    def populate(self, components: list[Component], filtered_components: list[Component] = None):
        self.clear()
        self.components = []

        for component in components:
            self.add_item(component=component)

        # update the proxy
        self.filtered_components = filtered_components or []
        self.proxy.set_filtered_components(components=self.filtered_components)

    def refresh(self):
        self.populate(components=self.components, filtered_components=self.filtered_components)

    def set_text_filter(self, text: str):
        text = text.replace(' ', '*')
        self.proxy.setFilterWildcard(text)


class ComponentListProxyModel(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.only_show_filtered_components: bool = True
        self.filtered_components: list[Component] = []

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex):
        print(f"{source_row = }")
        if not self.only_show_filtered_components:
            return super().filterAcceptsRow(source_row, source_parent)

        index = self.sourceModel().index(source_row, 0, source_parent)
        component = index.data(ComponentItemRoles.component)
        if component not in self.filtered_components:
            return False
        return super().filterAcceptsRow(source_row, source_parent)

    def set_filtered_components(self, components: list[Component]):
        self.filtered_components = components

    def set_only_show_filtered_components(self, show: bool):
        self.only_show_filtered_components: bool = show
        # TODO: refresh from here (ComponentListProxyModel.beginFilterChange() and endFilterChange() not found)
        #  until then re-call any other filter's application with same args
