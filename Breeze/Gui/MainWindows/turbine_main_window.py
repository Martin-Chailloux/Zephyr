from PySide6 import QtCore
from PySide6.QtWidgets import QMainWindow, QWidget, QListView, QSplitter, QVBoxLayout, QLabel

from Turbine.Gui.tb_select_process_panel import SelectProcessPanel
from Turbine.Gui.tb_steps_viewer import StepsViewer


class TurbineGui(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        alignment = QtCore.Qt.AlignmentFlag
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(alignment.AlignTop | alignment.AlignLeft)

        v_splitter = QSplitter()
        layout.addWidget(v_splitter)

        select_process_panel = SelectProcessPanel()
        v_splitter.addWidget(select_process_panel)

        steps_viewer_panel = StepsViewer()
        v_splitter.addWidget(steps_viewer_panel)

        self.select_process_panel = select_process_panel
        self.steps_viewer_panel = steps_viewer_panel

    def _connect_signals(self):
        self.select_process_panel.jobs_list.job_selected.connect(self.on_job_selected)

    def on_job_selected(self):
        job = self.select_process_panel.jobs_list.get_selected_job()
        self.steps_viewer_panel.populate(job=job)
