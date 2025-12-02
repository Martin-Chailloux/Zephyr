from PySide6.QtCore import Signal

from Api.document_models.project_documents import Stage
from Api.document_models.studio_documents import Software
from Gui.mvd.abstract_mvd import AbstractListView
from Gui.mvd.software_mvd.software_list_item_delegate import SoftwareListItemDelegate
from Gui.mvd.software_mvd.software_list_model import SoftwareListModel, SoftwareItemRoles


class SoftwareListView(AbstractListView):
    software_selected = Signal(str)
    right_clicked = Signal()

    def __init__(self, stage: Stage):
        super().__init__()
        self._model = SoftwareListModel(stage=stage)
        self.setModel(self._model)

        self._item_delegate = SoftwareListItemDelegate()
        self.setItemDelegate(self._item_delegate)

    def get_software(self) -> Software:
        index = self.get_selected_index()
        software: Software = index.data(SoftwareItemRoles.software)
        return software
