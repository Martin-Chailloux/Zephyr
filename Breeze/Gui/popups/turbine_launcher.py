from typing import Optional, Type, Any

import qtawesome
from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QStackedWidget, QLabel

from Api.breeze_app import BreezeApp
from Api.document_models.project_documents import Version, Component, Stage
from Api.document_models.studio_documents import Process

from Gui.mvd.stage_mvd.stage_list_view import StageListViewMinimal
from Gui.popups.abstract_popup_widget import AbstractPopupWidget
from Gui.mvd.process_mvd.process_list_view import ProcessListView
from Gui.sub_widgets.asset_widgets.asset_browser_widget import AssetBrowserWidget

from Api.turbine.gui import GuiBase
from Api.turbine.step import EngineBase
from Api.turbine.utils import JobContext


class TurbineLauncher(AbstractPopupWidget):
    process_finished = Signal()

    def __init__(self, component: Component, version: Optional[Version], process: Process = None, inputs: dict[str, Any] = None):
        super().__init__(w=280, show_borders=True)
        self.setWindowTitle("Select a process to launch with turbine")

        self.process_cache = _ProcessCache()
        self.inputs_cache = _InputsCache()
        if process is not None and inputs is not None:
            self.inputs_cache.set_item(stage=component.stage, process=process, inputs=inputs)

        self.previous_stage: Optional[Stage] = None  # inputs_cache hack
        self.previous_process: Optional[Process] = None  # inputs_cache hack

        self.source_context = JobContext(
            user=BreezeApp.user,
            component=component,
            version=version,
        )

        self.engine: Optional[EngineBase] = None

        self._init_ui()
        self._connect_signals()
        self._init_state()

        if process is not None:
            self.process_list.select_process(process=process)


    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # asset browser
        asset_browser = AssetBrowserWidget(show_bookmark=False)
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
        self.on_process_selected()

    def set_engine(self, engine: EngineBase):
        self.engine = engine

    def get_gui(self) -> GuiBase:
        gui: GuiBase = self.gui_widget.widget(0)
        return gui

    def set_gui(self, gui: GuiBase = None):
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

        # cache
        row = self.process_cache.get_row(stage=self.stage_list.stage)
        self.process_list.select_row(row)  # TODO: remember rows with a cache

    def on_process_selected(self):
        """ displays the ui matching the selected process """

        stage = self.stage_list.stage
        process: Process = self.process_list.get_selected_process()

        # process cache
        row: int = self.process_list.get_selected_index().row()
        self.process_cache.set_item(stage=stage, row=row)

        # inputs cache
        gui = self.get_gui()
        if gui is not None:
            self.inputs_cache.set_item(stage=self.previous_stage, process=self.previous_process, inputs=gui.export_inputs())

        if process is None:
            self.set_gui(None)
        else:
            engine = EngineBase.from_database(process=process, context=self.get_current_context())
            inputs = self.inputs_cache.get_inputs(stage=stage, process=process)
            engine.gui.import_inputs(inputs=inputs)
            self.set_gui(gui=engine.gui)
            self.set_engine(engine=engine)

        self.previous_stage = stage
        self.previous_process = process

    def get_current_context(self) -> JobContext:
        stage = self.stage_list.stage
        component = stage.get_work_component()
        # TODO: strange because the version comes from the inputs in the end, maybe the context could only be the component
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

    def on_launch_button_clicked(self):
        # TODO:
        #  - test with a long process
        #  - launch in a separate thread and debug
        inputs = self.get_gui().get_inputs()
        engine = self.engine
        engine.context.update_from_inputs(inputs=inputs)
        engine.context.set_creation_time()

        engine.run()

        self.process_finished.emit()
        self.accept()


class _ProcessCache:
    def __init__(self):
        self.items: dict[str, int] = {}

    def clear(self):
        self.items = {}

    def set_item(self, stage: Stage, row: int):
        self.items[stage.longname] = row

    def get_row(self, stage: Stage) -> int:
        row = self.items.get(stage.longname, 0)
        return row


class _InputsCache:
    def __init__(self):
        self.items: dict[str, dict] = {}

    def clear(self):
        self.items = {}

    @staticmethod
    def _get_key(stage: Stage, process: Process) -> str:
        key = f"{stage.longname}_{process.longname}"
        return key

    def set_item(self, stage: Stage, process: Process, inputs: dict):
        if stage is None or process is None:
            return
        key = self._get_key(stage=stage, process=process)
        self.items[key] = inputs

    def get_inputs(self, stage: Stage, process: Process) -> dict:
        key = self._get_key(stage=stage, process=process)
        inputs = self.items.get(key, {})
        return inputs
