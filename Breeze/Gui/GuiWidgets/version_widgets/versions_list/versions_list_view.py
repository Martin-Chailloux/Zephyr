from PySide6.QtCore import Signal

from Data.project_documents import Collection
from Gui.GuiWidgets.abstract_widgets.abstract_mvd import AbstractListView
from Gui.GuiWidgets.version_widgets.versions_list.versions_list_item_delegate import VersionListItemDelegate
from Gui.GuiWidgets.version_widgets.versions_list.versions_list_model import VersionListModel


class VersionListView(AbstractListView):
    software_selected = Signal(str)
    right_clicked = Signal()

    def __init__(self, collection: Collection = None):
        super().__init__()
        self._model = VersionListModel(collection=collection)
        self.setModel(self._model)

        self._item_delegate = VersionListItemDelegate()
        self.setItemDelegate(self._item_delegate)

    def set_collection(self, collection: Collection):
        self._model.collection = collection
        self._model.populate()
        self.viewport().update()

    def refresh(self):
        print(f"REFRESH: {self.__class__.__name__}")
        # re-query the collection else it might not be up to date
        collection = Collection.objects.get(longname=self._model.collection.longname)
        self.set_collection(collection)

