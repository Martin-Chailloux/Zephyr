from PySide6.QtWidgets import QWidget, QVBoxLayout

from Api.breeze_app import BreezeApp
from Api.project_documents import Asset
from Gui.sub_widgets.asset_widgets.asset_selector_widget import AssetSelectorWidget
from Gui.sub_widgets.stage_templates_widgets.stage_list_widget import StageListWidget


class AssetBrowserPanel(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self.init_state()
        self.connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        project = BreezeApp.project

        select_asset_widget = AssetSelectorWidget(project)
        layout.addWidget(select_asset_widget)

        stage_list_widget = StageListWidget(asset=select_asset_widget.current_asset)
        layout.addWidget(stage_list_widget)

        self.select_asset_widget = select_asset_widget
        self.stage_list_widget = stage_list_widget

    def connect_signals(self):
        self.select_asset_widget.asset_selected.connect(self.on_asset_selected)

    def on_asset_selected(self, longname: str):
        if not longname:
            asset = None
        else:
            asset = Asset.objects.get(longname=longname)
        self.stage_list_widget.set_current_asset(asset)

    def init_state(self):
        asset = self.select_asset_widget.current_asset
        self.stage_list_widget.stage_list_view.set_asset(asset)
