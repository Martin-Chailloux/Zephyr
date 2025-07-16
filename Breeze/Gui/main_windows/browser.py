import qtawesome

from PySide6 import QtCore
from PySide6.QtWidgets import QMainWindow, QDockWidget

from Api.project_documents import Stage
from Gui.panels.browser.asset_browser_panel import AssetBrowserPanel
from Gui.panels.browser.selected_stage_panel import SelectedStagePanel


class BrowserGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Breeze")
        self.setWindowIcon(qtawesome.icon("fa5s.wind"))
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        # asset browse
        asset_browser_panel = AssetBrowserPanel()
        dock = QDockWidget("Select Stage")
        dock.setWidget(asset_browser_panel)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, dock)
        dock.setAllowedAreas(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea)

        # selected stage
        selected_stage_panel = SelectedStagePanel()
        self.setCentralWidget(selected_stage_panel)

        # public vars
        self.asset_browser_panel = asset_browser_panel
        self.selected_stage_panel = selected_stage_panel

    def _connect_signals(self):
        self.asset_browser_panel.asset_selected.connect(self._on_asset_selected)
        self.asset_browser_panel.stage_selected.connect(self._on_stage_selected)

        # match stage data between asset_browser_panel and selected_stage_panel
        self.asset_browser_panel.stage_data_modified.connect(self.refresh_selected_stage_banner)
        self.selected_stage_panel.stage_data_modified.connect(self.refresh_asset_stage_list)

    def _on_asset_selected(self):
        """ selects the same stage as the stage from selected_stage_panel """
        selected_stage = self.selected_stage_panel.stage
        stages = self.asset_browser_panel.asset_stages
        if selected_stage in stages:
            self.asset_browser_panel.select_stage(stage=selected_stage)

    def _on_stage_selected(self):
        """ updates the selected_stage_panel's current stage """
        stage = self.asset_browser_panel.selected_stage
        self.selected_stage_panel.set_stage(stage=stage)

    def refresh_asset_stage_list(self):
        self.asset_browser_panel.refresh_stage_list()

    def refresh_selected_stage_banner(self):
        self.selected_stage_panel.refresh_banner()
