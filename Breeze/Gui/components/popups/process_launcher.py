from typing import Optional

import qtawesome
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QStackedWidget, QWidget

from Api.breeze_app import BreezeApp
from Api.project_documents import Version, Component, JobContext
from Api.turbine.inputs_ui import ProcessInputsUi
from Gui.components.mvd.stage_mvd.stage_list_view import StageListEditableView, StageListMinimalView
from Gui.components.popups.abstract_popup_widget import AbstractPopupWidget
from Gui.components.mvd.process_mvd.process_list_view import ProcessListView
from Api.turbine.process import ProcessBase
from Gui.sub_widgets.asset_widgets.asset_browser_widget import AssetBrowserWidget


class ProcessSelectMenu(AbstractPopupWidget):
    process_finished = Signal()

    def __init__(self, component: Component, version: Optional[Version]):
        super().__init__(w=280, show_borders=True)
        self.setWindowTitle("Select a process to launch")
        self.Context = JobContext(
            user=BreezeApp.user,
            component=component,
            version=version,
        )
        self._init_ui()
        self._connect_signals()
        self._init_state()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        asset_browser = AssetBrowserWidget(show_favorite=False)
        layout.addWidget(asset_browser)

        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)
        h = 148

        stage_list = StageListMinimalView()
        h_layout.addWidget(stage_list)
        stage_list.setFixedWidth(160)
        stage_list.setFixedHeight(h)

        process_list = ProcessListView()
        h_layout.addWidget(process_list)
        process_list.setFixedHeight(h)

        stacked_widget = QStackedWidget()
        layout.addWidget(stacked_widget)

        launch_button = QPushButton("Launch")
        layout.addWidget(launch_button)
        launch_button.setIcon(qtawesome.icon('fa.rocket'))
        launch_button.setFixedHeight(32)

        self.asset_browser = asset_browser
        self.stage_list = stage_list

        self.ui_widget = stacked_widget
        self.process_list = process_list
        self.launch_button = launch_button

    def _connect_signals(self):
        self.asset_browser.asset_selected.connect(self.on_asset_selected)

        self.stage_list.right_clicked.connect(self.reject)
        self.stage_list.stage_selected.connect(self.on_stage_selected)

        self.process_list.process_selected.connect(self.on_process_selected)
        self.process_list.right_clicked.connect(self.reject)
        self.launch_button.clicked.connect(self.on_launch_button_clicked)

    def _init_state(self):
        self.asset_browser.set_asset(longname=self.Context.component.stage.asset.longname)
        self.on_asset_selected()  # only needed if current asset is the first from the list
        self.stage_list.select_stage(stage=self.Context.component.stage)

    def on_asset_selected(self):
        asset = self.asset_browser.asset
        self.stage_list.set_asset(asset)

    def on_stage_selected(self):
        stage = self.stage_list.stage
        self.process_list.set_stage_template(stage_template=self.stage_list.stage.stage_template)
        self.process_list.select_row(0)  # TODO: improve with a cache

        self.Context.set_component(component=stage.work_component)

    def set_process_ui(self, widget: ProcessInputsUi = None):
        current_widget = self.ui_widget.widget(0)
        self.ui_widget.removeWidget(current_widget)

        if widget is not None:
            self.ui_widget.insertWidget(0, widget)

    def on_process_selected(self):
        """ displays the ui matching the selected process """
        process: ProcessBase.__class__ = self.process_list.process

        if process is None:
            self.set_process_ui(None)
            return

        if process.Ui is None:
            self.set_process_ui(ProcessInputsUi(label="- Inputs not found -"))
        else:
            self.set_process_ui(process.Ui(context=self.Context))

    def on_launch_button_clicked(self):
        process: ProcessBase.__class__ = self.process_list.process
        self.Context.update_creation_time()  # update datetime to match the moment the process is launched

        process = process(context=self.Context, ui=self.ui_widget.widget(0))

        process.run()
        print(f"Launching process: {process = }")
        self.process_finished.emit()
        self.accept()
