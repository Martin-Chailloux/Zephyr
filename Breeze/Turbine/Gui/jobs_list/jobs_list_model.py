from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtGui import QStandardItem, QStandardItemModel

from Data.project_documents import Job


@dataclass
class JobItemRoles:
    job = QtCore.Qt.ItemDataRole.UserRole


@dataclass
class JobItemMetrics:
    padding: int = 8
    height: int = 52
    user_w: int = height + padding - 4
    version_w: int = user_w + 32 + padding
    datetime_w: int = 56


class JobsListModel(QStandardItemModel):
    def __init__(self):
        super().__init__()
        self.jobs: list[Job] = []

    def add_item(self, job: Job):
        row = self.rowCount()

        item = QStandardItem()
        item.setSizeHint(QSize(0, JobItemMetrics.height))
        item.setEditable(False)

        item.setData(job, JobItemRoles.job)
        item.setToolTip(job.source_process.tooltip)

        self.setItem(row, item)
        self.jobs.append(job)

    def populate(self, jobs: list[Job]):
        self.clear()
        self.jobs = []

        jobs = sorted(jobs, key=lambda x: x.creation_time, reverse=True)
        for job in jobs:
            self.add_item(job=job)

    def refresh(self):
        self.populate(self.jobs)
