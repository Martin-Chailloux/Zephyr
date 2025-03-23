import qtawesome

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QPushButton, QDialog, QVBoxLayout, QListWidget, QListWidgetItem, QCheckBox, QListView, \
    QHBoxLayout

from Data.software import SoftwareModel
from Gui.util_widgets.searchbar_widgets import SearchbarWidget


class SelectSoftwarePopup(QDialog):
    def __init__(self, available_soft: list[SoftwareModel], recommended_soft: list[SoftwareModel]):
        super().__init__()
        self.available_soft = available_soft
        self.recommended_soft = recommended_soft
        self.recommended_soft_labels = [s.label.lower() for s in self.recommended_soft]

        self.setWindowTitle("Choose a software")
        self.setWindowIcon(qtawesome.icon("fa5s.rocket"))
        self._init_ui()
        self.set_initial_state()
        self.connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        sub_layout = QHBoxLayout()
        layout.addLayout(sub_layout)

        # searchbar_widget
        searchbar_widget = SearchbarWidget()
        sub_layout.addWidget(searchbar_widget)

        # 'show all' checkbox
        show_all_checkbox = QCheckBox("Show all")
        sub_layout.addWidget(show_all_checkbox)

        # software grid
        software_grid = IconsGrid()
        layout.addWidget(software_grid)
        for i, soft in enumerate(self.available_soft):
            soft = soft
            item = QListWidgetItem(soft.label)
            item.setIcon(soft.icon)
            software_grid.addItem(item)

        sub_layout = QHBoxLayout()
        layout.addLayout(sub_layout)
        sub_layout.setSpacing(1)

        # cancel button
        cancel_button = QPushButton("Cancel")
        sub_layout.addWidget(cancel_button)
        cancel_button.setFixedHeight(24)
        cancel_button.setIcon(qtawesome.icon('fa.close'))

        # confirm button
        confirm_button = QPushButton("Confirm")
        sub_layout.addWidget(confirm_button)
        confirm_button.setFixedHeight(24)
        confirm_button.setIcon(qtawesome.icon('fa.check'))

        # ------------------------
        # public vars
        # ------------------------
        self.searchbar_widget = searchbar_widget
        self.show_all_checkbox = show_all_checkbox
        self.software_grid = software_grid

    def connect_signals(self):
        self.searchbar_widget.textChanged.connect(self.update_visible_items)
        self.show_all_checkbox.clicked.connect(self.update_visible_items)

    def update_visible_items(self):
        text_filter = self.searchbar_widget.text()
        for item in self.software_grid.all_items:
            is_hidden_by_filter = text_filter.lower() not in item.text().lower()
            is_recommended = item.text().lower() in self.recommended_soft_labels
            is_hidden_by_checkbox = not self.show_all_checkbox.isChecked() and not is_recommended

            is_hidden = is_hidden_by_filter or is_hidden_by_checkbox
            item.setHidden(is_hidden)

    def set_initial_state(self):
        self.update_visible_items()


class IconsGrid(QListWidget):
    columns = 5

    def __init__(self):
        super().__init__()
        self.setViewMode(QListView.ViewMode.IconMode)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setLayoutMode(QListView.LayoutMode.Batched)
        self.setUniformItemSizes(True)

    @property
    def all_items(self) -> list[QListWidgetItem]:
        items = [self.item(i) for i in range(self.count())]
        return items

    def _resize(self):
        """
        Set grid and icon size based on the number of columns.
        (inspired from qtawesome's icon_browser.py)
        """

        width = self.viewport().width() - 30
        # The minus 30 above ensures we don't end up with an item width that
        # can't be drawn the expected number of times across the view without
        # being wrapped. Without this, the view can flicker during resize
        tile_w = int(width / self.columns)
        icon_w = int(width / self.columns * 0.8)

        self.setGridSize(QSize(tile_w, tile_w))
        self.setIconSize(QSize(icon_w, icon_w))

        for item in self.all_items:
            item.setSizeHint(QSize(tile_w, tile_w))

    def resizeEvent(self, event):
        self._resize()
        super().resizeEvent(event)
