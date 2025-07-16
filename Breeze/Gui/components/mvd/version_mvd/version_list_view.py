import qtawesome
from PySide6.QtCore import Signal, Qt, QPoint, QItemSelectionModel
from PySide6.QtWidgets import QMenu

from Api.project_documents import Component, Version
from Gui.components.mvd.abstract_mvd import AbstractListView
from Gui.components.mvd.version_mvd.version_list_item_delegate import VersionListItemDelegate
from Gui.components.mvd.version_mvd.version_list_model import VersionListModel, VersionItemRoles


class VersionListView(AbstractListView):
    software_selected = Signal(str)
    right_clicked = Signal()

    def __init__(self):
        super().__init__()
        self._model = VersionListModel()
        self.setModel(self._model)

        self._item_delegate = VersionListItemDelegate()
        self.setItemDelegate(self._item_delegate)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def set_collection(self, collection: Component):
        if collection is None:
            versions = []
        else:
            versions = collection.versions

        self._model.populate(versions=versions)
        self.viewport().update()

    def get_selected_version(self) -> Version | None:
        items = self.selected_items
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
        file = version.to_file()
        file.open_interactive()
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
            version.copy_filepath()
        elif requested_action is open_folder_action:
            version.open_folder()

        else:
            return
