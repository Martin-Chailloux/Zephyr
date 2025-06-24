import importlib

from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtGui import QMouseEvent

from Data.project_documents import Job
from Gui.GuiWidgets.abstract_widgets.abstract_mvd import AbstractListView
from Turbine.Gui.jobs_list.jobs_list_item_delegate import JobsListItemDelegate
from Turbine.Gui.jobs_list.jobs_list_model import JobItemRoles, JobsListModel


class JobsListView(AbstractListView):
    job_selected = Signal(str)
    right_clicked = Signal()

    def __init__(self):
        super().__init__()
        self._model = JobsListModel()
        self.setModel(self._model)

        self._item_delegate = JobsListItemDelegate()
        self.setItemDelegate(self._item_delegate)

        self.selectionModel().selectionChanged.connect(self.on_selection_changed)

    def mousePressEvent(self, event):
        if isinstance(event, QMouseEvent):
            if event.button() == QtCore.Qt.MouseButton.RightButton:
                self.right_clicked.emit()
                return

        super().mousePressEvent(event)

    def set_jobs(self):
        # TODO: filters: user, time, searchbar
        jobs = Job.objects()
        self._model.populate(jobs=jobs)

    def get_selected_job(self) -> Job | None:
        items = self.get_selected_items()
        if not items:
            return None
        else:
            job: Job = items[0].data(JobItemRoles.job)
            return job

    def on_selection_changed(self):
        job = self.get_selected_job()
        print(f"Selected: {job = }")
        self.job_selected.emit(job)
