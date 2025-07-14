from PySide6.QtWidgets import QWidget, QVBoxLayout

from Api.breeze_app import BreezeApp
from Api.project_documents import Stage
from Gui.sub_widgets.asset_widgets.asset_selector_widget import AssetSelectorWidget
from Gui.sub_widgets.stage_widgets.stage_list_widget import StageListWidget


class AssetBrowserPanel(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._init_state()
        self._connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        project = BreezeApp.project

        asset_selector_widget = AssetSelectorWidget(project)
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

    def _connect_signals(self):
        self.asset_selector_widget.asset_selected.connect(self._on_asset_selected)

    def _on_asset_selected(self):
        asset = self.asset_selector_widget.asset
        self.stage_list_widget.stage_list.set_asset(asset=asset)

    def _init_state(self):
        self._on_asset_selected()
