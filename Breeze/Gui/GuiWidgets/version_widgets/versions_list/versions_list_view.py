import subprocess

import qtawesome
from PySide6.QtCore import Signal, Qt, QPoint
from PySide6.QtWidgets import QMenu

from Data import breeze_converters
from Data.project_documents import Collection, Version
from Gui.GuiWidgets.abstract_widgets.abstract_mvd import AbstractListView
from Gui.GuiWidgets.version_widgets.versions_list.versions_list_item_delegate import VersionListItemDelegate
from Gui.GuiWidgets.version_widgets.versions_list.versions_list_model import VersionListModel, VersionItemRoles


class VersionListView(AbstractListView):
    software_selected = Signal(str)
    right_clicked = Signal()

    def __init__(self, collection: Collection = None):
        super().__init__()
        self._model = VersionListModel(collection=collection)
        self.setModel(self._model)

        self._item_delegate = VersionListItemDelegate()
        self.setItemDelegate(self._item_delegate)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def set_collection(self, collection: Collection):
        self._model.collection = collection
        self._model.populate()
        self.viewport().update()

    def refresh(self):
        print(f"REFRESH: {self.__class__.__name__}")
        # re-query the collection else it might not be up to date
        collection = Collection.objects.get(longname=self._model.collection.longname)
        self.set_collection(collection)

    def get_selected_version(self) -> Version | None:
        items = self.get_selected_items()
        if not items:
            return None
        version = items[0].data(VersionItemRoles.version)
        return version

    def get_hovered_version(self) -> Version:
        item = self.get_hovered_item()
        version = item.data(VersionItemRoles.version)
        return version

    def mouseDoubleClickEvent(self, event):
        version = self.get_hovered_version()

        # get matching Software's instance
        software_instance = breeze_converters.get_file_instance_from_software(
            software=version.software,
            filepath=version.filepath
        )
        software_instance.open_interactive()
        print(f"Opening {version.software.label} file: {version.filepath}")

    def show_context_menu(self, position: QPoint):
        # TODO: rmb -> exit, remove close button if done
        version = self.get_hovered_version()

        # create menu
        menu = QMenu()
        close_action = menu.addAction("Close")
        close_action.setIcon(qtawesome.icon('fa.close'))
        menu.addSeparator()
        copy_path_action = menu.addAction("Copy filepath")
        copy_path_action.setIcon(qtawesome.icon('fa5s.copy'))
        open_folder_action = menu.addAction("Open folder")
        open_folder_action.setIcon(qtawesome.icon('fa5s.folder-open'))

        # open menu
        requested_action = menu.exec_(self.mapToGlobal(position))

        # result
        if requested_action is copy_path_action:
            version.open_folder()
        elif requested_action is open_folder_action:
            version.copy_filepath()
        else:
            return
