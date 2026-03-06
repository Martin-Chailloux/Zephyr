from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtGui import QStandardItem

from Api.document_models.studio_documents import Project
from Gui.mvd.abstract_mvd import AbstractItemModel


@dataclass
class ProjectItemRoles:
    project = QtCore.Qt.ItemDataRole.UserRole


@dataclass
class ProjectItemMetrics:
    height: int = 48


class ProjectListModel(AbstractItemModel):
    def __init__(self):
        super().__init__()
        self.projects: list[Project] = []

    def add_item(self, project: Project):
        row = self.rowCount()

        item = QStandardItem()
        item.setSizeHint(QSize(0, ProjectItemMetrics.height))
        item.setEditable(False)

        item.setData(project, ProjectItemRoles.project)

        self.setItem(row, item)

    def populate(self, projects: list[Project]):
        self.projects = projects
        self.clear()

        for project in projects:
            self.add_item(project)
