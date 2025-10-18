from PySide6.QtCore import Signal, QSize

from Api.document_models.project_documents import Job
from Gui.mvd.abstract_mvd import AbstractListView
from Gui.mvd.job_mvd.job_list_item_delegate import JobListItemDelegate
from Gui.mvd.job_mvd.job_list_model import JobItemRoles, JobListModel


class JobListView(AbstractListView):
    job_selected = Signal()

    def __init__(self):
        super().__init__()
        self._model = JobListModel()
        self.setModel(self._model)

        self._item_delegate = JobListItemDelegate()
        self.setItemDelegate(self._item_delegate)

        self.selectionModel().selectionChanged.connect(self.on_selection_changed)

        self._init_state()

    def _init_state(self):
        self.resize(QSize(400, self.height()))

    def get_jobs(self):
        # TODO: filters: user, time, searchbar
        self.blockSignals(True)
        jobs = Job.objects()
        self._model.populate(jobs=jobs)
        self.blockSignals(False)

    def get_selected_job(self) -> Job | None:
        items = self.selected_items
        if not items:
            return None
        else:
            job: Job = items[0].data(JobItemRoles.job)
            return job

    def on_selection_changed(self):
        self.job_selected.emit()
