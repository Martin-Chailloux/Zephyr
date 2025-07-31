import importlib

from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtGui import QMouseEvent

from Api.studio_documents import Process, StageTemplate
from Gui.components.mvd.abstract_mvd import AbstractListView
from Gui.components.mvd.process_mvd.process_list_item_delegate import ProcessListItemDelegate
from Gui.components.mvd.process_mvd.process_list_model import ProcessListModel, ProcessItemRoles
from Api.turbine.process import ProcessBase


class ProcessListView(AbstractListView):
    process_selected = Signal(str)
    right_clicked = Signal()

    def __init__(self):
        super().__init__()
        self._model = ProcessListModel()
        self.setModel(self._model)

        self._item_delegate = ProcessListItemDelegate()
        self.setItemDelegate(self._item_delegate)

        self.selectionModel().selectionChanged.connect(self.on_selection_changed)

    def mousePressEvent(self, event):
        if isinstance(event, QMouseEvent):
            if event.button() == QtCore.Qt.MouseButton.RightButton:
                self.right_clicked.emit()
                return

        super().mousePressEvent(event)

    def set_stage_template(self, stage_template: StageTemplate):
        self._model.populate(processes=stage_template.processes)

    @property
    def process(self) -> ProcessBase.__class__ | None:
        items = self.selected_items
        if not items:
            return None
        else:
            process: Process = items[0].data(ProcessItemRoles.process)
            return process.to_class()

    def on_selection_changed(self):
        self.process_selected.emit(self.process)
