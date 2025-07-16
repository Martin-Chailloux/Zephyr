from typing import Optional

import qtawesome
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QPushButton

from Api.breeze_app import BreezeApp
from Api.project_documents import Version, Component
from Gui.components.popups.abstract_popup_widget import AbstractPopupWidget
from Gui.components.mvd.process_mvd.process_list_view import ProcessListView
from Api.turbine import ProcessBase


class ProcessSelectMenu(AbstractPopupWidget):
    process_finished = Signal()

    def __init__(self, component: Component, version: Optional[Version]):
        super().__init__(w=168, h=248, position=[0.5, 1])
        self.component = component
        self.version = version
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        process_list = ProcessListView()
        layout.addWidget(process_list)
        process_list.set_stage_template(stage_template=self.component.stage.stage_template)

        launch_button = QPushButton("Launch")
        layout.addWidget(launch_button)
        launch_button.setIcon(qtawesome.icon('fa.rocket'))
        launch_button.setFixedHeight(32)

        self.processes_list = process_list
        self.launch_button = launch_button

    def _connect_signals(self):
        self.processes_list.process_selected.connect(self.on_process_selected)
        self.processes_list.right_clicked.connect(self.reject)
        self.launch_button.clicked.connect(self.on_launch_button_clicked)

    def on_process_selected(self, pseudo: str):
        # TODO: update ui on the right side with process infos + inputs
        pass
        # process = MgPR.objects.get(pseudo=pseudo)
        # self.accept()

    def on_launch_button_clicked(self):
        process: ProcessBase.__class__ = self.processes_list.get_selected_process()
        process = process(user=BreezeApp.user, component=self.component, version=self.version)
        process.run()
        print(f"Launching process: {process = }")
        self.process_finished.emit()
