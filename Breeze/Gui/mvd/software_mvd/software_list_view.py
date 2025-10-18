from PySide6.QtCore import Signal

from Api.project_documents import Stage
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

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        hovered_item = self.get_hovered_item()
        if hovered_item is None:
            return
        software = hovered_item.data(SoftwareItemRoles.software)
        self.software_selected.emit(software.label)
