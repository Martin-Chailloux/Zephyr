from datetime import datetime
from typing import Optional

import qtawesome
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QStackedWidget, QWidget, QLabel

from Api.breeze_app import BreezeApp
from Api.project_documents import Version, Component, JobContext
from Api.turbine.inputs_ui import ProcessInputsUi
from Gui.components.popups.abstract_popup_widget import AbstractPopupWidget
from Gui.components.mvd.process_mvd.process_list_view import ProcessListView
from Api.turbine.process import ProcessBase


class ProcessSelectMenu(AbstractPopupWidget):
    process_finished = Signal()

    def __init__(self, component: Component, version: Optional[Version]):
        super().__init__(w=360, h=256, position=[0.5, 1], show_borders=True)
        self.setWindowTitle("Select a process to launch")
        self.Context = JobContext(
            user=BreezeApp.user,
            component=component,
            version=version,
        )
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)

        process_list = ProcessListView()
        h_layout.addWidget(process_list)
        process_list.set_stage_template(stage_template=self.Context.component.stage.stage_template)
        process_list.setFixedWidth(128)

        sub_layout = QVBoxLayout()
        h_layout.addLayout(sub_layout)

        ui_title = QLabel()
        sub_layout.addWidget(ui_title)

        stacked_widget = QStackedWidget()
        sub_layout.addWidget(stacked_widget)

        launch_button = QPushButton("Launch")
        layout.addWidget(launch_button)
        launch_button.setIcon(qtawesome.icon('fa.rocket'))
        launch_button.setFixedHeight(32)

        self.ui_title = ui_title
        self.ui_widget = stacked_widget
        self.processes_list = process_list
        self.launch_button = launch_button

    def _connect_signals(self):
        self.processes_list.process_selected.connect(self.on_process_selected)
        self.processes_list.right_clicked.connect(self.reject)
        self.launch_button.clicked.connect(self.on_launch_button_clicked)

    def set_process_ui(self, widget: QWidget = None):
        current_widget = self.ui_widget.widget(0)
        self.ui_widget.removeWidget(current_widget)

        if widget is not None:
            self.ui_widget.insertWidget(0, widget)

    def on_process_selected(self):
        """ displays the ui matching the selected process """
        process: ProcessBase.__class__ = self.processes_list.get_selected_process()

        if process is None:
            self.set_process_ui(None)
            self.ui_title.setText("")
            return

        self.ui_title.setText(process.label)
        if process.Ui is None:
            self.set_process_ui(ProcessInputsUi())
        else:
            self.set_process_ui(process.Ui(context=self.Context))

    def on_launch_button_clicked(self):
        process: ProcessBase.__class__ = self.processes_list.get_selected_process()
        self.Context.update_creation_time()  # update datetime to match the moment the process is launched
        process = process(context=self.Context, ui=self.ui_widget.widget(0))
        process.run()
        print(f"Launching process: {process = }")
        self.process_finished.emit()
        self.accept()
