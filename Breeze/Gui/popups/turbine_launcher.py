from typing import Optional, Type

import qtawesome
from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QStackedWidget, QLabel

from Api.breeze_app import BreezeApp
from Api.document_models.project_documents import Version, Component
from Api.document_models.studio_documents import Process

from Gui.mvd.stage_mvd.stage_list_view import StageListViewMinimal
from Gui.popups.abstract_popup_widget import AbstractPopupWidget
from Gui.mvd.process_mvd.process_list_view import ProcessListView
from Gui.sub_widgets.asset_widgets.asset_browser_widget import AssetBrowserWidget

from Api.turbine.engine_inputs_gui import EngineGuiBase
from Api.turbine.step import TurbineEngine
from Api.turbine.utils import JobContext


class TurbineLauncher(AbstractPopupWidget):
    process_finished = Signal()

    def __init__(self, component: Component, version: Optional[Version]):
        super().__init__(w=280, show_borders=True)
        self.setWindowTitle("Select a process to launch with turbine")
        self.source_context = JobContext(
            user=BreezeApp.user,
            component=component,
            version=version,
        )
        self.engine: Optional[TurbineEngine] = None
        self._init_ui()
        self._connect_signals()
        self._init_state()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # asset browser
        asset_browser = AssetBrowserWidget(show_favorite=False)
        layout.addWidget(asset_browser)

        # stage list
        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)

        h = 148
        stage_list = StageListViewMinimal()
        h_layout.addWidget(stage_list)
        stage_list.setFixedWidth(160)
        stage_list.setFixedHeight(h)

        # process list
        process_list = ProcessListView()
        h_layout.addWidget(process_list)
        process_list.setFixedHeight(h)

        # selected process inputs
        inputs_title = QLabel("Inputs:")
        layout.addWidget(inputs_title)

        layout.addStretch()

        sub_layout = QVBoxLayout()
        layout.addLayout(sub_layout)
        sub_layout.setContentsMargins(7, 7, 7, 7)

        stacked_widget = QStackedWidget()
        sub_layout.addWidget(stacked_widget)

        # launch button
        launch_button = QPushButton("Launch")
        layout.addWidget(launch_button)
        launch_button.setIcon(qtawesome.icon('fa.rocket'))
        launch_button.setFixedHeight(32)

        self.asset_browser = asset_browser
        self.stage_list = stage_list

        self.gui_widget = stacked_widget
        self.process_list = process_list
        self.launch_button = launch_button

    def _connect_signals(self):
        self.asset_browser.asset_selected.connect(self.on_asset_selected)

        self.stage_list.right_clicked.connect(self.reject)
        self.stage_list.stage_selected.connect(self.on_stage_selected)

        self.process_list.selectionModel().selectionChanged.connect(self.on_process_selected)
        self.process_list.right_clicked.connect(self.reject)
        self.launch_button.clicked.connect(self.on_launch_button_clicked)

    def _init_state(self):
        self.asset_browser.set_asset(longname=self.source_context.component.stage.asset.longname)
        self.on_asset_selected()  # only needed if current asset is the first from the list
        self.stage_list.select_stage(stage=self.source_context.component.stage)

    def set_engine(self, engine: TurbineEngine):
        self.engine = engine

    def get_gui(self) -> EngineGuiBase:
        gui: EngineGuiBase = self.gui_widget.widget(0)
        return gui

    def set_gui(self, gui: EngineGuiBase = None):
        self.gui_widget.removeWidget(self.get_gui())
        if gui is None:
            return
        self.gui_widget.insertWidget(0, gui)

    def on_asset_selected(self):
        asset = self.asset_browser.asset
        self.stage_list.set_asset(asset)

    def on_stage_selected(self):
        self.process_list.selectionModel().blockSignals(True)
        self.process_list.set_stage_template(stage_template=self.stage_list.stage.stage_template)
        self.process_list.selectionModel().blockSignals(False)
        self.process_list.select_row(0)  # TODO: remember rows with a cache

    def get_current_context(self) -> JobContext:
        stage = self.stage_list.stage
        component = stage.get_work_component()
        # TODO: cache to remember selected versions for each component, initiated with the source context
        if component == self.source_context.component:
            version = self.source_context.version
        else:
            version = None

        context = JobContext(
            user=self.source_context.user,
            component=component,
            version=version,
        )

        return context

    def on_process_selected(self):
        """ displays the ui matching the selected process """
        process: Process = self.process_list.get_selected_process()
        if process is None:
            self.set_gui(None)
        else:
            engine = TurbineEngine.from_database(process=process, context=self.get_current_context())
            self.set_gui(gui=engine.gui)
            self.set_engine(engine=engine)

    def on_launch_button_clicked(self):
        inputs = self.get_gui().inputs
        engine = self.engine
        engine.context.update_from_inputs(inputs=inputs)
        engine.context.set_creation_time()

        engine.run()

        self.process_finished.emit()
        self.accept()
