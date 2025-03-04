from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout

from MangoEngine import project_dialog
from MangoEngine.document_models import Project, Asset
from Panels.select_stage.select_asset_widget import SelectAssetWidget
from Panels.select_stage.stage_list import StageListWidget


class SelectStagePanel(QWidget):
    stage_selected = Signal(str)

    def __init__(self):
        super().__init__()
        self._init_ui()
        self.init_state()
        self.connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        project: Project = project_dialog.get_project("Dev")
        select_asset_widget = SelectAssetWidget(project)
        layout.addWidget(select_asset_widget)

        stage_list_widget = StageListWidget()
        layout.addWidget(stage_list_widget)

        self.select_asset_widget = select_asset_widget
        self.stage_list_widget = stage_list_widget

    def connect_signals(self):
        self.select_asset_widget.asset_selected.connect(self.on_asset_selected)
        self.stage_list_widget.stage_selected.connect(self.on_stage_selected)

    def on_asset_selected(self, longname: str):
        asset = Asset.objects.get(longname=longname)
        self.stage_list_widget.set_asset(asset)

    def on_stage_selected(self, longname: str):
        self.stage_selected.emit(longname)

    def init_state(self):
        asset = self.select_asset_widget.current_asset
        self.stage_list_widget.set_asset(asset)