import qtawesome
from PySide6.QtGui import QStandardItem
from PySide6.QtWidgets import QTreeWidget, QVBoxLayout, QTreeWidgetItem, QPushButton, QComboBox, QHeaderView, QCheckBox

from Api.project_documents import Component


class IngredientTopItem(QTreeWidgetItem):
    def __init__(self, label: str):
        super().__init__()

        self.setText(0, label)

        new_button = QPushButton()
        new_button.setIcon(qtawesome.icon('fa.plus-circle'))

        self.new_button = new_button


class IngredientSubItem(QTreeWidgetItem):
    def __init__(self, component: Component):
        super().__init__()

        version_numbers = [f"{version.number:03d}" for version in component.versions]
        version_numbers.sort(reverse=True)

        use_last_version = QCheckBox()
        use_last_version.setChecked(True)

        combobox = QComboBox()
        combobox.addItems(version_numbers)
        combobox.setFixedWidth(64)

        self.component = component
        self.use_last_version_checkbox = use_last_version
        self.combobox = combobox


class IngredientsTreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHeaderHidden(True)
        self.setColumnCount(3)
        self.setColumnWidth(0, 400)

        self.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.header().setStretchLastSection(False)

        self._init_content()
        self.expandAll()

        for component in Component.objects:
            self.add_component(parent=self.free_components_top_item, component=component)

    def _init_content(self):
        free_components_top_item = self.add_top_item(label="Free components")

        self.free_components_top_item = free_components_top_item

    def add_top_item(self, label: str) -> IngredientTopItem:
        item = IngredientTopItem(label=label)

        new_button_item = QTreeWidgetItem()
        item.addChild(new_button_item)
        self.setItemWidget(new_button_item, 0, item.new_button)

        self.addTopLevelItem(item)

        return item

    def add_component(self, parent: QTreeWidgetItem, component: Component) -> IngredientSubItem:
        item = IngredientSubItem(component=component)

        parent.insertChild(0, item)
        item.setText(0, component.longname)
        self.setItemWidget(item, 1, item.use_last_version_checkbox)
        self.setItemWidget(item, 2, item.combobox)

        return item