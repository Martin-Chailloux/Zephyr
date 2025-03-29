from PySide6.QtWidgets import QWidget, QVBoxLayout

from Data.breeze_documents import Project, Asset
from Dialogs import projects_dialog
from Gui.asset_widgets.select_asset_widget import SelectAssetWidget
from Gui.stages_widgets.stage_list import StageListWidget
from Gui.stages_widgets.stages_list.stages_list_view import StageListView


class SelectStagePanel(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self.init_state()
        self.connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        project: Project = projects_dialog.get_project("Dev")

        select_asset_widget = SelectAssetWidget(project)
        layout.addWidget(select_asset_widget)

        stage_list_widget = StageListView()
        layout.addWidget(stage_list_widget)

        self.select_asset_widget = select_asset_widget
        self.stage_list_widget = stage_list_widget

    def connect_signals(self):
        self.select_asset_widget.asset_selected.connect(self.on_asset_selected)

    def on_asset_selected(self, longname: str):
        asset = Asset.objects.get(longname=longname)
        self.stage_list_widget.set_asset(asset)

    def init_state(self):
        asset = self.select_asset_widget.current_asset
        self.stage_list_widget.set_asset(asset)
