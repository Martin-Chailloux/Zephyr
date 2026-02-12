from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QTabWidget, QPushButton

from Api.breeze_app import BreezeApp
from Api.document_models.project_documents import Stage, SubUser
from Gui.mvd.asset_mvd.asset_list_view import AssetListView
from Gui.sub_widgets.asset_widgets.asset_browser_widget import AssetBrowserWidget
from Gui.sub_widgets.stage_widgets.stage_list_widget import StageListWidget


class StageSelectorPanel(QWidget):
    asset_selected = Signal()
    stage_selected = Signal()
    stage_data_modified = Signal()

    def __init__(self):
        super().__init__()
        self._init_ui()
        self._init_state()
        self._connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        asset_selector_widget = AssetBrowserWidget()
        layout.addWidget(asset_selector_widget)

        splitter = QSplitter()
        splitter.setOrientation(QtCore.Qt.Orientation.Vertical)
        layout.addWidget(splitter)

        stage_list_widget = StageListWidget()
        splitter.addWidget(stage_list_widget)
        splitter.setCollapsible(0, False)

        quick_search_widget = BookmarksAndRecentAssetsWidget()
        splitter.addWidget(quick_search_widget)

        self.asset_selector_widget = asset_selector_widget
        self.stage_list_widget = stage_list_widget
        self.quick_search_widget = quick_search_widget

    @property
    def stages(self) -> list[Stage]:
        asset = self.asset_selector_widget.asset
        if asset is None:
            return []
        else:
            return asset.stages

    @property
    def selected_stage(self) -> Stage | None:
        return self.stage_list_widget.stage_list.stage

    def select_stage(self, stage: Stage = None):
        self.stage_list_widget.stage_list.select_stage(stage=stage)

    def _connect_signals(self):
        self.asset_selector_widget.asset_selected.connect(self._on_asset_selected)
        self.asset_selector_widget.asset_bookmarked.connect(self.quick_search_widget.refresh)

        self.stage_list_widget.stage_list.stage_selected.connect(self._on_stage_selected)
        self.stage_list_widget.stage_list.stage_data_modified.connect(self._on_stage_data_modified)

        self.quick_search_widget.asset_list.asset_data_modified.connect(self.asset_selector_widget.refresh)
        self.quick_search_widget.asset_list.asset_selected.connect(self.on_asset_quick_searched)

    def _on_asset_selected(self):
        asset = self.asset_selector_widget.asset
        self.stage_list_widget.set_asset(asset=asset)

        user = SubUser.current()
        user.add_recent_asset(asset=asset)

        self.quick_search_widget.refresh()

        self.asset_selected.emit()  # promote

    def _on_stage_selected(self):
        self.stage_selected.emit()  # promote

    def _on_stage_data_modified(self):
        self.stage_data_modified.emit()  # promote

    def on_asset_quick_searched(self):
        asset = self.quick_search_widget.asset_list.asset
        self.asset_selector_widget.select_asset(asset=asset)

    def _init_state(self):
        self._on_asset_selected()

    def refresh_stage_list(self):
        self.stage_list_widget.stage_list.refresh()

    def refresh(self):
        self.refresh_stage_list()


class BookmarksAndRecentAssetsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._connect_signals()
        self._init_state()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        switch_button = QPushButton('Bookmarks')
        layout.addWidget(switch_button)

        asset_list_widget = AssetListView()
        layout.addWidget(asset_list_widget)

        self.switch_button = switch_button
        self.asset_list = asset_list_widget

    def _connect_signals(self):
        self.switch_button.clicked.connect(self.switch)

    def _init_state(self):
        self.switch()

    def refresh(self):
        current = self.switch_button.text()
        match current:
            case 'Bookmarks':
                self.show_bookmarks()
            case 'Recent':
                self.show_recent()
            case _:
                raise ValueError(f"Unexpected display mode: {current}")

    def switch(self):
        previous_mode = self.switch_button.text()
        match previous_mode:
            case 'Bookmarks':
                self.show_recent()
            case 'Recent':
                self.show_bookmarks()
            case _:
                raise ValueError(f"Unexpected display mode: {previous_mode}")

    @staticmethod
    def get_sub_user() -> SubUser:
        sub_user = SubUser.current()
        return sub_user

    def show_recent(self):
        self.switch_button.setText('Recent')
        self.asset_list.set_assets(assets=self.get_sub_user().recent_assets)

    def show_bookmarks(self):
        self.switch_button.setText('Bookmarks')
        self.asset_list.set_assets(assets=self.get_sub_user().bookmarks)
