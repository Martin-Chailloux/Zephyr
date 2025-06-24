from dataclasses import dataclass

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtGui import QStandardItem, QStandardItemModel

from Data.studio_documents import Process


@dataclass
class ProcessItemRoles:
    process = QtCore.Qt.ItemDataRole.UserRole

@dataclass
class ProcessItemMetrics:
    height: int = 32


class ProcessListModel(QStandardItemModel):
    def __init__(self):
        super().__init__()

    def add_item(self, process: Process):
        row = self.rowCount()

        item = QStandardItem()
        item.setSizeHint(QSize(0, ProcessItemMetrics.height))
        item.setEditable(False)

        item.setData(process, ProcessItemRoles.process)

        self.setItem(row, item)

    def populate(self, processes: list[Process]):
        self.clear()
        for process in processes:
            self.add_item(process=process)

