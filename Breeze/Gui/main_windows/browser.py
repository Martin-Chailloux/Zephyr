import qtawesome

from PySide6 import QtCore
from PySide6.QtWidgets import QMainWindow, QDockWidget

from Gui.panels.browser.stage_selector_panel import StageSelectorPanel
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
        stage_selector_panel = StageSelectorPanel()
        dock = QDockWidget("Select Stage")
        dock.setWidget(stage_selector_panel)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, dock)
        dock.setAllowedAreas(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea)

        # selected stage
        selected_stage_panel = SelectedStagePanel()
        self.setCentralWidget(selected_stage_panel)

        # public vars
        self.stage_selector_panel = stage_selector_panel
        self.selected_stage_panel = selected_stage_panel

    def _connect_signals(self):
        self.stage_selector_panel.asset_selected.connect(self._on_asset_selected)
        self.stage_selector_panel.stage_selected.connect(self._on_stage_selected)

        # match stage data between asset_browser_panel and selected_stage_panel
        self.stage_selector_panel.stage_data_modified.connect(self.refresh_selected_stage_banner)
        self.selected_stage_panel.stage_data_modified.connect(self.refresh_asset_stage_list)

    def refresh(self):
        self.stage_selector_panel.refresh()
        self.selected_stage_panel.refresh()

    def _on_asset_selected(self):
        """ selects the same stage as the stage from selected_stage_panel """
        selected_stage = self.selected_stage_panel.stage
        stages = self.stage_selector_panel.stages
        if selected_stage in stages:
            self.stage_selector_panel.select_stage(stage=selected_stage)

    def _on_stage_selected(self):
        """ updates the selected_stage_panel's current stage """
        stage = self.stage_selector_panel.selected_stage
        self.selected_stage_panel.set_stage(stage=stage)

    def refresh_asset_stage_list(self):
        self.stage_selector_panel.refresh()

    def refresh_selected_stage_banner(self):
        self.selected_stage_panel.refresh_banner()
