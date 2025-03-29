from PySide6.QtCore import Signal
from PySide6.QtWidgets import QListView

from Data.breeze_documents import Asset
from Gui.stage_widgets.stages_list.stages_list_item_delegate import StageListItemDelegate
from Gui.stage_widgets.stages_list.stages_list_model import StageListModel

# TODO: recover edit stages button

class StageListView(QListView):
    stage_selected = Signal()

    def __init__(self):
        super().__init__()
        self._model = StageListModel()
        self._item_delegate = StageListItemDelegate()

        self.setModel(self._model)
        self.setItemDelegate(self._item_delegate)

    def set_asset(self, asset: Asset):
        self._model.set_asset(asset)
