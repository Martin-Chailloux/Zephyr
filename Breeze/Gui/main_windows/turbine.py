from PySide6 import QtCore
from PySide6.QtWidgets import QMainWindow, QLabel, QDockWidget

from Gui.panels.turbine.job_selector_panel import SelectProcessPanel
from Gui.panels.turbine.step_logs_panel import StepLogsPanel
from Gui.panels.turbine.steps_viewer_panel import StepsViewer


class TurbineGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        select_process_panel = SelectProcessPanel()
        dock = QDockWidget()
        dock.setWindowTitle("Jobs")
        dock.setWidget(select_process_panel)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, dock)
        dock.setAllowedAreas(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea)

        steps_viewer_panel = StepsViewer()
        self.setCentralWidget(steps_viewer_panel)

        logs_panel = StepLogsPanel()
        dock = QDockWidget()
        dock.setWindowTitle("Logs")
        dock.setWidget(logs_panel)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.BottomDockWidgetArea, dock)
        dock.setAllowedAreas(QtCore.Qt.DockWidgetArea.BottomDockWidgetArea)

        self.setCorner(QtCore.Qt.Corner.BottomLeftCorner, QtCore.Qt.DockWidgetArea.LeftDockWidgetArea)

        self.select_process_panel = select_process_panel
        self.steps_viewer_panel = steps_viewer_panel
        self.logs_panel = logs_panel

    def _connect_signals(self):
        self.select_process_panel.jobs_list.job_selected.connect(self.on_job_selected)
        self.steps_viewer_panel.step_selected.connect(self.on_step_selected)

    def on_job_selected(self):
        job = self.select_process_panel.jobs_list.get_selected_job()
        self.steps_viewer_panel.populate(job=job)

    def on_step_selected(self):
        log = self.steps_viewer_panel.selected_step_log
        print(f"{log = }")
        self.logs_panel.set_log(log=log)
