from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout

from Api.breeze_app import BreezeApp
from Api.project_documents import Stage
from Gui.sub_widgets.asset_widgets.asset_browser_widget import AssetBrowserWidget
from Gui.sub_widgets.stage_widgets.stage_list_widget import StageListWidget


class AssetBrowserPanel(QWidget):
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

        project = BreezeApp.project

        asset_selector_widget = AssetBrowserWidget()
        layout.addWidget(asset_selector_widget)

        stage_list_widget = StageListWidget()
        layout.addWidget(stage_list_widget)

        self.asset_selector_widget = asset_selector_widget
        self.stage_list_widget = stage_list_widget

    @property
    def asset_stages(self) -> list[Stage]:
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
        self.stage_list_widget.stage_list.stage_selected.connect(self._on_stage_selected)
        self.stage_list_widget.stage_list.stage_data_modified.connect(self._on_stage_data_modified)

    def _on_asset_selected(self):
        asset = self.asset_selector_widget.asset
        self.stage_list_widget.set_asset(asset=asset)

        self.asset_selected.emit()  # promote

    def _on_stage_selected(self):
        self.stage_selected.emit()  # promote

    def _on_stage_data_modified(self):
        self.stage_data_modified.emit()  # promote

    def _init_state(self):
        self._on_asset_selected()

    def refresh_stage_list(self):
        self.stage_list_widget.stage_list.refresh()

    def refresh(self):
        self.refresh_stage_list()
