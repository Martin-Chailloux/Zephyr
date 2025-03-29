from PySide6.QtWidgets import QListView

from Gui.version_widgets.versions_list.versions_list_item_delegate import VersionsListItemDelegate
from Gui.version_widgets.versions_list.versions_list_model import VersionsListModel


class VersionsListView(QListView):
    def __init__(self):
        super().__init__()
        self._model = VersionsListModel()
        self._item_delegate = VersionsListItemDelegate()

        self.setModel(self._model)
        self.setItemDelegate(self._item_delegate)

    def add_version(self, version):
        self._model.add_item(version)