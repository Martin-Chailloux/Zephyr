import qtawesome
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QComboBox, QLabel, QGridLayout

from Api.breeze_app import BreezeApp
from Api.document_models.project_documents import Asset
from Gui.popups.text_input_popup import TextInputPopup
from Gui.sub_widgets.asset_widgets.bookmark_widgets import BookmarkIconButton


# TODO: bug: if an asset without existing name or variant, the previous stage list is kept
# TODO: strange to use project here, categories should be deduced from a query

class AssetBrowserWidget(QWidget):
    h = 32
    add_item_label = "New"
    asset_selected = Signal()

    def __init__(self, show_favorite: bool=True):
        super().__init__()
        self.show_favorite = show_favorite
        self.cache = _SelectionCache()

        self._init_ui()
        self._connect_signals()
        self._on_category_selected()

    def _init_ui(self):
        self.setMaximumWidth(512)

        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setVerticalSpacing(1)
        grid_layout.setHorizontalSpacing(5)

        label = QLabel("Category")
        grid_layout.addWidget(label, 0, 0)

        category_cb = _AssetFieldCombobox(name="category")
        grid_layout.addWidget(category_cb, 1, 0)
        category_cb.set_items(BreezeApp.project.categories)

        label = QLabel("Name")
        grid_layout.addWidget(label, 0, 1)

        name_cb = _AssetFieldCombobox(name="name")
        grid_layout.addWidget(name_cb, 1, 1)

        label = QLabel("Variant")
        grid_layout.addWidget(label, 0, 3)

        variant_cb = _AssetFieldCombobox(name="variant")
        grid_layout.addWidget(variant_cb, 1, 3)

        for cb in [category_cb, name_cb, variant_cb]:
            cb.setFixedHeight(self.h)

        set_bookmark_button = BookmarkIconButton()
        if self.show_favorite:
            grid_layout.addWidget(set_bookmark_button, 1, 4)

        # ------------------------
        # public vars
        # ------------------------
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
    def asset(self) -> Asset | None:
        asset = Asset.objects(category=self.category, name=self.name, variant=self.variant)
        if not asset:
            return None
        elif len(asset) == 1:
            return asset[0]
        else:  # this is not supposed to happen
            raise ValueError(f"Found more than 1 asset: {asset = }")

    def set_asset(self, longname: str):
        asset = Asset.objects(longname=longname)
        if len(asset) != 1:
            raise ValueError(f"Could not find an asset with longname: {longname}")

        parts = longname.split("_")
        category = parts[0]
        name = parts[1]
        variant = parts[2]
        self.category_cb.setCurrentText(category)
        self.name_cb.setCurrentText(name)
        self.variant_cb.setCurrentText(variant)

    def _connect_signals(self):
        self.category_cb.currentTextChanged.connect(self._on_category_selected)
        self.name_cb.currentTextChanged.connect(self._on_name_selected)
        self.variant_cb.currentTextChanged.connect(self._on_variant_selected)

        self.category_cb.item_created.connect(self._on_category_created)
        self.name_cb.item_created.connect(self._on_name_created)
        self.variant_cb.item_created.connect(self._on_variant_created)

    def _on_category_selected(self):
        self.name_cb.blockSignals(True)  # Delay on_name_selected()

        assets = Asset.objects(category=self.category, variant="-")
        names = [asset.name for asset in assets]
        self.name_cb.set_items(names)

        name = self.cache.get_name(category=self.category)
        if name is not None:
            self.name_cb.setCurrentText(name)

        self._on_name_selected()

        self.name_cb.blockSignals(False)

    def _on_name_selected(self):
        self.variant_cb.blockSignals(True)

        assets = Asset.objects(category=self.category, name=self.name)
        variants = [asset.variant for asset in assets]
        self.variant_cb.set_items(variants)

        variant = self.cache.get_variant(category=self.category, name=self.name)
        if variant is not None:
            self.variant_cb.setCurrentText(variant)

        self._on_variant_selected()

        self.variant_cb.blockSignals(False)

    def _on_variant_selected(self):
        self.cache.set_key(self.category, self.name, self.variant)
        self.asset_selected.emit()

    def _on_category_created(self, category: str):
        print(f"CATEGORY CREATED: {category}")
        BreezeApp.project.add_category(category)
        self.category_cb.set_items(BreezeApp.project.categories)
        self.category_cb.setCurrentText(category)

    def _on_name_created(self, name: str):
        print(f"NAME CREATED: {name}")
        Asset.create(category=self.category, name=name)
        self._on_category_selected()
        self.name_cb.setCurrentText(name)

    def _on_variant_created(self, variant: str):
        print(f"VARIANT CREATED: {variant}")
        Asset.create(category=self.category, name=self.name, variant=variant)
        self._on_name_selected()
        self.variant_cb.setCurrentText(variant)


class _AssetFieldCombobox(QComboBox):
    add_item_label = "New"
    item_created = Signal(str)

    def __init__(self, name: str):
        super().__init__()
        self.name = name
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
                popup = TextInputPopup(
                    title=f"New {self.name}",
                    placeholder=f"new {self.name}",
                    forbidden_inputs = invalid_names,
                )
                popup.input_accepted.connect(self.on_new_selected)
                item_added = popup.show_menu(position=[0.5, 0.5])
                if not item_added:
                    self.setCurrentIndex(self.previous_index)

        self.previous_index = self.currentIndex()

    def on_new_selected(self, name: str):
        self.item_created.emit(name)


class _SelectionCache:
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
