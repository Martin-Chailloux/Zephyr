from typing import Optional

from PySide6.QtCore import Signal

from Api.document_models.project_documents import Component, Version
from Gui.mvd.abstract_mvd import AbstractListView
from Gui.mvd.version_mvd.version_list_item_delegate import VersionListItemDelegate
from Gui.mvd.version_mvd.version_list_model import VersionListModel, VersionItemRoles


class VersionListView(AbstractListView):
    software_selected = Signal(str)

    def __init__(self):
        super().__init__()
        self._model = VersionListModel()
        self.setModel(self._model.proxy)

        self._item_delegate = None
        self.set_item_delegate()

    def set_item_delegate(self):  # can be sub-classed if needed
        self._item_delegate = VersionListItemDelegate()
        self.setItemDelegate(self._item_delegate)

    # setters
    def set_component(self, component: Optional[Component], clear_cache: bool=False):
        if clear_cache:
            component.reload()
        if component is None:
            versions = []
        else:
            versions = component.versions

        self._model.populate(versions=versions)
        self.viewport().update()

    def set_versions(self, versions: list[Version]):
        self._model.populate(versions=versions)
        self.viewport().update()

    # getters
    def get_selected_version(self) -> Version | None:
        index = self.get_selected_index()
        if index is None:
            return None
        version = index.data(VersionItemRoles.version)
        return version

    def get_hovered_version(self) -> Version | None:
        index = self._get_hovered_index()
        if index is None:
            return None
        version = index.data(VersionItemRoles.version)
        return version

    def set_text_filter(self, text: str):
        self._model.set_text_filter(text=text)