from PySide6 import QtCore
from PySide6.QtCore import QSize, QPoint
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox,
                               QTextEdit, QHBoxLayout, QSizePolicy)

from Api.document_models.project_documents import Job
from Gui.popups.turbine_launcher import TurbineLauncher
from Gui.sub_widgets.context_menu import ContextMenu
from Utils.sub_widgets import IconButton
from Gui.mvd.job_mvd.job_list_view import JobListView


class SelectJobPanel(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        # layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)

        refresh_button = IconButton(icon_name='fa.refresh')
        layout.addWidget(refresh_button)

        sub_layout = QHBoxLayout()
        layout.addLayout(sub_layout)

        user_picture = QLabel()
        sub_layout.addWidget(user_picture)
        user_picture.setFixedSize(QSize(36, 36))

        time_combobox = QComboBox()
        sub_layout.addWidget(time_combobox)
        time_combobox.addItems(["Today", "Yesterday", "Last 7 days", "Last 30 days", "All"])

        search_bar = QTextEdit()
        layout.addWidget(search_bar)
        search_bar.setFixedHeight(32)
        search_bar.setPlaceholderText("Search")

        layout.addSpacing(12)

        jobs_list = JobListView()
        layout.addWidget(jobs_list)
        jobs_list.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        jobs_list.get_jobs()
        jobs_list.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)

        self.refresh_button = refresh_button
        self.jobs_list = jobs_list

    def _connect_signals(self):
        self.refresh_button.clicked.connect(self.refresh)
        self.jobs_list.customContextMenuRequested.connect(self.show_context_menu)

    def refresh(self):
        self.jobs_list.get_jobs()

    def show_context_menu(self, position: QPoint):
        job = self.jobs_list.get_hovered_job()
        menu = JobsSelectorContextMenu(job=job)
        menu.show(position=self.jobs_list.mapToGlobal(position))


class JobsSelectorContextMenu(ContextMenu):
    def __init__(self, job: Job):
        super().__init__()
        self.job = job

        self.relaunch_action = self.add_action(label="Relaunch", icon_name='fa5s.address-card')

    def resolve(self, action: QAction):
        match action:
            case self.relaunch_action:
                self.relaunch_job()
            case _:
                return

    def relaunch_job(self):
        source_version = self.job.source_version
        turbine_launcher = TurbineLauncher(component=source_version.component, version=source_version,
                                           process=self.job.source_process, inputs=self.job.inputs)
        result = turbine_launcher.show_menu(position=[0.5, 0.5])
