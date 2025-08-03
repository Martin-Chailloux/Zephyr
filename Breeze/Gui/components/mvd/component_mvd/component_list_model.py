from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtCore import QSize, QSortFilterProxyModel
from PySide6.QtGui import QStandardItem, QStandardItemModel

from Api.project_documents import Component


@dataclass
class ComponentItemRoles:
    component = QtCore.Qt.ItemDataRole.UserRole


@dataclass
class ComponentItemMetrics:
    height: int = 36
    stage_w = 64


class ComponentListModel(QStandardItemModel):
    def __init__(self):
        super().__init__()
        self.components: list[Component] = []
        self.proxy = QSortFilterProxyModel()
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

    def populate(self, components: list[Component]):
        self.clear()
        self.components = []

        for job in components:
            self.add_item(component=job)

    def refresh(self):
        self.populate(self.components)

    def set_text_filter(self, text: str):
        text = text.replace(' ', '*')
        self.proxy.setFilterWildcard(text)
