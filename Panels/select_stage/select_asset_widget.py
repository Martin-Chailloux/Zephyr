import qtawesome
from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel, QGridLayout, QFrame

from MangoEngine import mongo_dialog
from MangoEngine.document_models import Project, Asset
from Widgets.line_edit_popup import LineEditPopup
from Utils.chronometer import Chronometer

from Widgets.favorite_widgets import SetFavoriteIconButton


# TODO: if an asset without existing name or variant, the previous stage list is kept

class SelectAssetWidget(QWidget):
    h = 32
    add_item_label = "New"
    asset_selected = Signal(str)

    def __init__(self, project: Project):
        super().__init__()
        self.project = project
        chronometer = Chronometer()

        chronometer.tick("GSelectStageWidget built in")

        self.cache = SelectionCache()

        self._init_ui()
        self.connect_signals()
        self.on_category_selected()

    def _init_ui(self):
        self.setMaximumWidth(512)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)

        # ==============
        # grid
        # ==============
        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)
        grid_layout.setContentsMargins(7, 7, 7, 7)
        grid_layout.setVerticalSpacing(1)
        grid_layout.setHorizontalSpacing(5)

        label = QLabel("Category")
        grid_layout.addWidget(label, 0, 0)

        category_cb = AssetFieldCombobox()
        grid_layout.addWidget(category_cb, 1, 0)
        category_cb.set_items(self.project.categories)

        label = QLabel("Name")
        grid_layout.addWidget(label, 0, 1)

        name_cb = AssetFieldCombobox()
        grid_layout.addWidget(name_cb, 1, 1)

        label = QLabel("Variant")
        grid_layout.addWidget(label, 0, 3)

        variant_cb = AssetFieldCombobox()
        grid_layout.addWidget(variant_cb, 1, 3)

        fav = SetFavoriteIconButton()
        grid_layout.addWidget(fav, 1, 4)

        # ==============
        # stages
        # ==============
        line = QFrame()
        layout.addWidget(line)
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)

        for cb in [category_cb, name_cb, variant_cb]:
            cb.setFixedHeight(self.h)

        # ==============
        # public vars
        # ==============
        self.category_cb = category_cb
        self.name_cb = name_cb
        self.variant_cb = variant_cb

    @property
    def category(self) -> str:
        return self.category_cb.currentText()

    @property
    def name(self) -> str:
        return self.name_cb.currentText()

    @property
    def variant(self) -> str:
        return self.variant_cb.currentText()

    @property
    def current_asset(self) -> Asset:
        current_asset =  Asset.objects.get(category=self.category, name=self.name, variant=self.variant)
        print(f"{current_asset = }")
        return current_asset

    def connect_signals(self):
        self.category_cb.currentTextChanged.connect(self.on_category_selected)
        self.name_cb.currentTextChanged.connect(self.on_name_selected)
        self.variant_cb.currentTextChanged.connect(self.on_variant_selected)

        self.category_cb.item_created.connect(self.on_category_created)
        self.name_cb.item_created.connect(self.on_name_created)
        self.variant_cb.item_created.connect(self.on_variant_created)

    def on_category_selected(self):
        self.name_cb.blockSignals(True)  # Delay on_name_selected()

        assets = mongo_dialog.get_asset(category=self.category, variant="-")
        names = [asset.name for asset in assets]
        self.name_cb.set_items(names)

        name = self.cache.get_name(category=self.category)
        if name is not None:
            self.name_cb.setCurrentText(name)

        self.on_name_selected()

        self.name_cb.blockSignals(False)

    def on_name_selected(self):
        self.variant_cb.blockSignals(True)

        assets = mongo_dialog.get_asset(category=self.category, name=self.name)
        variants = [asset.variant for asset in assets]
        self.variant_cb.set_items(variants)

        variant = self.cache.get_variant(category=self.category, name=self.name)
        if variant is not None:
            self.variant_cb.setCurrentText(variant)

        self.on_variant_selected()

        self.variant_cb.blockSignals(False)

    def on_variant_selected(self):
        self.cache.set_key(self.category, self.name, self.variant)

        forbidden = [self.add_item_label, ""]
        for s in self.category, self.name, self.variant:
            if s in forbidden:
                return

        variant = "-" if self.variant == "main" else self.variant
        self.asset_selected.emit(self.current_asset.longname)

    def on_category_created(self, category: str):
        print(f"CATEGORY CREATED: {category}")
        self.project.add_category(category)
        self.category_cb.set_items(self.project.categories)
        self.category_cb.setCurrentText(category)

    def on_name_created(self, name: str):
        print(f"NAME CREATED: {name}")
        mongo_dialog.create_asset(category=self.category, name=name)
        self.on_category_selected()
        self.name_cb.setCurrentText(name)

    def on_variant_created(self, variant: str):
        print(f"VARIANT CREATED: {variant}")
        mongo_dialog.create_asset(category=self.category, name=self.name, variant=variant)
        self.on_name_selected()
        self.variant_cb.setCurrentText(variant)


class AssetFieldCombobox(QComboBox):
    add_item_label = "New"
    item_created = Signal(str)

    def __init__(self):
        super().__init__()
        self.is_scrolling: bool = False
        self.previous_index: int = 0
        self.currentIndexChanged.connect(self.on_index_changed)

    @property
    def items(self) -> list[str]:
        items = [self.itemText(i) for i in range(self.count())]
        return items

    def set_items(self, items: list[str]):
        self.clear()

        if not items:
            items = [""]

        lowers = [item.lower() for item in items]
        items = [x for _, x in sorted(zip(lowers, items))]

        self.addItems(items)
        self.addItem(self.add_item_label)
        self.setItemIcon(self.count()-1, qtawesome.icon("fa.plus-circle"))

    def wheelEvent(self, event):
        # Loop at extremities & skip "new"
        self.is_scrolling = True

        previous_index = self.currentIndex()
        super().wheelEvent(event)

        wheel_up = event.angleDelta().y() > 0
        if wheel_up and previous_index == self.currentIndex():
            self.setCurrentIndex(self.count()-2)
        elif not wheel_up and previous_index == self.count()-2:
            self.setCurrentIndex(0)

        self.is_scrolling = False

    def on_index_changed(self):
        if not self.is_scrolling:
            if self.currentText() == self.add_item_label:
                invalid_names = self.items
                popup = LineEditPopup(title="New", invalid_entries=invalid_names)
                popup.create_clicked.connect(self.on_new_selected)

                item_added = popup.exec()
                if not item_added:
                    self.setCurrentIndex(self.previous_index)

        self.previous_index = self.currentIndex()

    def on_new_selected(self, name: str):
        self.item_created.emit(name)


class SelectionCache:
    """
    Remembers previous selections
    """
    def __init__(self):
        self.name_cache: dict[str, str] = {}
        self.variant_cache: dict[str, dict[str, str]] = {}

    def __repr__(self):
        return f"AssetCache: \n  - Names: {str(self.name_cache)} \n  - Variants: {str(self.variant_cache)}"

    def clear(self):
        self.name_cache = {}
        self.variant_cache = {}

    def set_key(self, category: str, name: str, variant: str):
        self.name_cache[category] = name

        if category not in self.variant_cache:
            self.variant_cache[category] = {}
        self.variant_cache[category][name] = variant

    def get_name(self, category: str) -> str | None:
        name = None

        if category in self.name_cache:
            name = self.name_cache[category]

        return name

    def get_variant(self, category: str, name: str) -> str | None:
        variant = None

        if category in self.variant_cache:
            if name in self.variant_cache[category]:
                variant =  self.variant_cache[category][name]

        return variant
