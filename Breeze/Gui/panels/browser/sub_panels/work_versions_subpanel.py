from PySide6 import QtCore
from PySide6.QtCore import Signal, QPoint
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget, QMenu

from Api.document_models.project_documents import Stage, Version
from Gui.popups.turbine_launcher import TurbineLauncher
from Gui.sub_widgets.context_menu import ContextMenu
from Gui.sub_widgets.toolbar import ToolBar
from Gui.panels.browser.sub_panels import work_versions_api
from Gui.mvd.version_mvd.version_list_view import VersionListView


class WorkVersionsWidget(QWidget):
    h = 28
    buttons_spacing = 2
    ask_refresh_exports = Signal()  # TODO: clean out

    def __init__(self, stage: Stage=None):
        super().__init__()
        self.stage = stage
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)

        # title
        label = QLabel("Work versions")
        layout.addWidget(label)

        # sub layout
        sub_layout = QHBoxLayout()
        layout.addLayout(sub_layout)

        # toolbar
        toolbar = VersionsBrowserToolBar()
        sub_layout.addWidget(toolbar)

        # versions list
        versions_list = VersionListView()
        versions_list.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        sub_layout.addWidget(versions_list)

        # public vars
        self.toolbar = toolbar
        self.versions_list = versions_list

    def set_stage(self, stage: Stage):
        self.stage = stage
        if stage is None:
            return

        self.versions_list.set_component(component=stage.get_work_component())
        self.versions_list.select_row(row=0, is_selected=True)

    def _connect_signals(self):
        self.toolbar.refresh_button.clicked.connect(self.refresh)
        self.toolbar.new_version_button.clicked.connect(self.create_empty_version)
        self.toolbar.increment_button.clicked.connect(self.increment_selected_version)
        self.toolbar.edit_comment_button.clicked.connect(self.edit_comment)
        self.toolbar.turbine_button.clicked.connect(self.launch_turbine_browser)

        self.versions_list.selectionModel().selectionChanged.connect(self.on_selection_changed)
        self.versions_list.double_clicked.connect(self.open_selected_version)
        self.versions_list.customContextMenuRequested.connect(self.show_context_menu)

        self.ask_refresh_exports.connect(self.refresh)

    def on_selection_changed(self):
        selected_indexes = self.versions_list.selectedIndexes()

        for button in [self.toolbar.increment_button, self.toolbar.turbine_button, self.toolbar.edit_comment_button]:
            button.setEnabled(len(selected_indexes) > 0)

    def refresh(self, select_last_version: bool=False, reselect_row: bool=False):
        # TODO: args are confusing to use
        if self.stage is None:
            return

        if self.stage.get_work_component() is not None:
            selected_index = self.versions_list.get_selected_index()
            if selected_index is None:
                current_row = 0
            else:
                current_row = selected_index.row()
            self.versions_list.set_component(component=self.stage.get_work_component(), clear_cache=True)
            if select_last_version:
                self.versions_list.select_row(row=0, is_selected=True)
            elif reselect_row:
                self.versions_list.select_row(current_row, is_selected=True)

    def create_empty_version(self):
        if self.stage is None:
            return

        confirm = work_versions_api.create_empty_version(stage=self.stage)
        if not confirm:
            return

        self.refresh(select_last_version=True)

    def open_selected_version(self):
        version = self.versions_list.get_hovered_version()
        version.open_interactive()

    def show_context_menu(self, position: QPoint):
        version = self.versions_list.get_hovered_version()
        menu = VersionsBrowserContextMenu(version=version)
        menu.show(position=self.versions_list.mapToGlobal(position))

    def increment_selected_version(self):
        if self.stage is None:
            return

        old_version = self.versions_list.get_selected_version()
        if old_version is None:
            return

        confirm = work_versions_api.increment(old_version=old_version)
        if not confirm:
            return

        self.refresh(select_last_version=True)

    def edit_comment(self):
        if self.stage is None:
            return

        version = self.versions_list.get_selected_version()
        work_versions_api.edit_comment(version=version)

        self.refresh(reselect_row=True)

    def launch_turbine_browser(self):
        if self.stage is None:
            return
        turbine_launcher = TurbineLauncher(component=self.stage.get_work_component(), version=self.versions_list.get_selected_version())
        # turbine_launcher.process_finished.connect(self.ask_refresh_exports.emit)
        result = turbine_launcher.show_menu(position=[0.5, 0.5])
        if result:
            self.refresh(reselect_row=True)


class VersionsBrowserToolBar(ToolBar):
    def _init_ui(self):
        self.refresh_button = self.add_button(icon_name='fa.refresh', tooltip='Refresh')
        self.add_divider()
        self.new_version_button = self.add_button(icon_name='fa.plus', tooltip='New: create an empty file')
        self.increment_button = self.add_button(icon_name='fa.arrow-up', tooltip='Increment: create an incremented copy of the selected version')
        self.edit_comment_button = self.add_button(icon_name='fa5s.comment-dots', tooltip='Comment: edit the comment of the selected versions')
        self.add_divider()
        self.turbine_button = self.add_button(icon_name='fa.gears', tooltip='Turbine: choose a process to launch')


class VersionsBrowserContextMenu(ContextMenu):
    def __init__(self, version: Version):
        super().__init__()
        self.version = version

        self.copy_id_action = self.add_action(label="Copy ID", icon_name='fa5s.address-card')
        self.copy_filepath_action = self.add_action(label="Copy filepath", icon_name='fa5s.copy')
        self.open_folder_action = self.add_action(label="Open folder", icon_name='fa5s.folder-open')

    def resolve(self, action: QAction):
        match action:
            case self.copy_id_action:
                self.version.copy_longname()
            case self.copy_filepath_action:
                self.version.copy_filepath()
            case self.open_folder_action:
                self.version.open_folder()
            case _:
                return
