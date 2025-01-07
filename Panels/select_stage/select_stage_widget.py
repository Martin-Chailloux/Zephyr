import qtawesome
from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QHBoxLayout, QComboBox, QLabel, QGridLayout, \
    QPushButton, QSpacerItem, QFrame

from Manghost import mongo_dialog
from Utils.chronometer import Chronometer

from Panels.select_stage.stage_list import ZStageListWidget
from Widgets.favorite_widgets import GSetFavoriteButton
from Widgets.header_widget import ZHeader


class GSelectStageWidget(QWidget):
    # TODO: TABS should be guessed from database
    TABS: list[str] = ["Character", "Props", "Element", "Decor", "Sequence", "Sandbox", "Library"]
    h = 32

    def __init__(self):
        super().__init__()
        chronometer = Chronometer()

        chronometer.tick("GSelectStageWidget built in")
        # self.assets = mongo_dialog.get_asset(category__in=self.TABS, variant="-")

        self.cache = SelectionCache()

        self._init_ui()
        self.connect_signals()


    def _init_ui(self):
        self.setFixedWidth(417)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)

        header = ZHeader(text="SELECT STAGE", icon_name="ri.arrow-down-s-fill")
        layout.addWidget(header)

        # --------------------
        # --- Testing zone ---
        # --------------------
        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)

        label = QLabel("Category")
        grid_layout.addWidget(label, 0, 0)

        category_cb = ComboBox()
        grid_layout.addWidget(category_cb, 1, 0)
        category_cb.set_items(self.TABS)

        # new_category_button = NewButton(text="New")
        # grid_layout.addWidget(new_category_button, 2, 0)

        label = QLabel("Name")
        grid_layout.addWidget(label, 0, 1)

        name_cb = ComboBox()
        grid_layout.addWidget(name_cb, 1, 1)

        # new_category_button = NewButton(text="New")
        # grid_layout.addWidget(new_category_button, 2, 1)

        label = QLabel("Variant")
        grid_layout.addWidget(label, 0, 3)

        variation_cb = ComboBox()
        grid_layout.addWidget(variation_cb, 1, 3)
        variation_cb.addItem("default")

        fav = GSetFavoriteButton(size=self.h, checkable=True)
        grid_layout.addWidget(fav, 1, 4)
        # fav.setFixedWidth()
        # fav.setFixedSize(QSize(self.h, self.h))
        # fav.setIconSize(QSize(self.h - 5, self.h - 5))

        # new_category_button = NewButton(text="New")
        # grid_layout.addWidget(new_category_button, 2, 3)
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        layout.addWidget(ZStageListWidget())

        for cb in [category_cb, name_cb, variation_cb]:
            cb.setFixedHeight(self.h)

        # --------------------

        # tab_widget = QTabWidget()
        # layout.addWidget(tab_widget)
        #
        # tabs = {}
        # for category in self.TABS:
        #     tabs[category]: dict[str, Asset] = [a for a in self.assets if a.category == category]
        #
        # for category, assets in tabs.items():
        #     tab = CategoryTab(category=category, assets=assets)
        #     tab_widget.addTab(tab, category.title())

        self.category_cb = category_cb
        self.name_cb = name_cb
        self.variant_cb = variation_cb

    @property
    def category(self) -> str:
        return self.category_cb.currentText()

    @property
    def name(self) -> str:
        return self.name_cb.currentText()

    @property
    def variant(self) -> str:
        return self.variant_cb.currentText()

    def connect_signals(self):
        self.category_cb.currentTextChanged.connect(self.on_category_selected)
        self.name_cb.currentTextChanged.connect(self.on_name_selected)
        self.variant_cb.currentTextChanged.connect(self.on_variant_selected)

    def on_category_selected(self):
        print(f"CATEGORY SELECTED: {self.category}")
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
        print(f"NAME SELECTED: {self.name}")
        self.variant_cb.blockSignals(True)

        assets = mongo_dialog.get_asset(category=self.category, name=self.name)
        variants = [asset.variant for asset in assets]
        if variants:
            variants[0] = "default"  # display "default" rather than "-"
        self.variant_cb.set_items(variants)

        variant = self.cache.get_variant(category=self.category, name=self.name)
        if variant is not None:
            self.variant_cb.setCurrentText(variant)

        self.on_variant_selected()

        self.variant_cb.blockSignals(False)

    def on_variant_selected(self):
        print(f"VARIANT SELECTED: {self.variant}")
        self.cache.set_key(self.category, self.name, self.variant)


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


class ComboBox(QComboBox):
    add_item_label = "New"
    # TODO: Connect with popup

    def __init__(self):
        super().__init__()

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
        # Loop at extremities while skipping "new"
        self.blockSignals(True)
        previous_index = self.currentIndex()
        super().wheelEvent(event)

        wheel_up = event.angleDelta().y() > 0
        if previous_index == 0 and wheel_up:
            self.setCurrentIndex(self.count()-2)
        elif self.currentText() == self.add_item_label:
            self.setCurrentIndex(0)

        self.blockSignals(False)