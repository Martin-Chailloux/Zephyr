from PySide6.QtCore import Signal

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

