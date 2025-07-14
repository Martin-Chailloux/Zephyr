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
        self.connect_signals()

    def _init_ui(self):
        # stage central widget
        selected_stage_panel = SelectedStagePanel()
        self.setCentralWidget(selected_stage_panel)

        # stage select
        asset_browser_panel = AssetBrowserPanel()
        dock = QDockWidget("Select Stage")
        dock.setWidget(asset_browser_panel)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, dock)
        dock.setAllowedAreas(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea)

        # public vars
        self.asset_browser_panel = asset_browser_panel
        self.selected_stage_panel = selected_stage_panel

    def connect_signals(self):
        self.asset_browser_panel.asset_selector_widget.asset_selected.connect(self.on_asset_selected)
        self.asset_browser_panel.stage_list_widget.stage_list.stage_selected.connect(self.on_stage_selected)

        self.asset_browser_panel.stage_list_widget.stage_list.stage_data_modified.connect(self.refresh_versions_stage)
        self.selected_stage_panel.stage_banner_widget.stage_list.stage_data_modified.connect(self.refresh_stage_list)

    def on_asset_selected(self):
        selected_stage = self.selected_stage_panel.stage_banner_widget.stage

        stages = self.asset_browser_panel.asset_stages
        if selected_stage in stages:
            self.asset_browser_panel.stage_list_widget.stage_list.select_stage(stage=selected_stage)

    def on_stage_selected(self):
        stage = self.asset_browser_panel.stage_list_widget.stage_list.selected_stage
        self.selected_stage_panel.set_stage(stage=stage)

    def refresh_stage_list(self):
        self.asset_browser_panel.stage_list_widget.stage_list.refresh()

    def refresh_versions_stage(self):
        self.selected_stage_panel.stage_banner_widget.stage_list.refresh()
