from PySide6.QtCore import Signal
from mkdocs.config.config_options import Optional

from Api.document_models.studio_documents import Process, StageTemplate
from Gui.mvd.abstract_mvd import AbstractListView
from Gui.mvd.process_mvd.process_list_item_delegate import ProcessListItemDelegate
from Gui.mvd.process_mvd.process_list_model import ProcessListModel, ProcessItemRoles
from Api.turbine.step import EngineBase


class ProcessListView(AbstractListView):
    def __init__(self):
        super().__init__()
        self._model = ProcessListModel()
        self.setModel(self._model)

        self._item_delegate = ProcessListItemDelegate()
        self.setItemDelegate(self._item_delegate)

    def set_stage_template(self, stage_template: StageTemplate):
        self._model.populate(processes=stage_template.processes)

    def get_selected_process(self) -> Process | None:
        index = self.get_selected_index()
        if index is None:
            return None
        process: Process = index.data(ProcessItemRoles.process)

        return process

    def select_process(self, process: Process):
        if process is None:
            self.selectionModel().clearSelection()
            return

        for row in range(self._model.rowCount()):
            index = self._model.index(row, 0)
            if process == index.data(ProcessItemRoles.process):
                self.select_row(row)
