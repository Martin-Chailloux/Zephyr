from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtGui import QMouseEvent

from Api.project_documents import Job
from Gui.components.mvd.abstract_mvd import AbstractListView
from Gui.components.mvd.job_mvd.job_list_item_delegate import JobListItemDelegate
from Gui.components.mvd.job_mvd.job_list_model import JobItemRoles, JobListModel


class JobListView(AbstractListView):
    job_selected = Signal(str)
    right_clicked = Signal()

    def __init__(self):
        super().__init__()
        self._model = JobListModel()
        self.setModel(self._model)

        self._item_delegate = JobListItemDelegate()
        self.setItemDelegate(self._item_delegate)

        self.selectionModel().selectionChanged.connect(self.on_selection_changed)

    def mousePressEvent(self, event):
        if isinstance(event, QMouseEvent):
            if event.button() == QtCore.Qt.MouseButton.RightButton:
                self.right_clicked.emit()
                return

        super().mousePressEvent(event)

    def get_jobs(self):
        # TODO: filters: user, time, searchbar
        self.blockSignals(True)
        jobs = Job.objects()
        self._model.populate(jobs=jobs)
        self.blockSignals(False)

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
