import qtawesome
from PySide6 import QtCore
from PySide6.QtCore import Signal, QPoint
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget, QMenu

from Api.document_models.project_documents import Stage
from Gui.popups.process_launcher import ProcessSelectMenu
from Utils.sub_widgets import PushButtonAutoWidth
from Gui.panels.browser.sub_panels import work_versions_api
from Gui.mvd.version_mvd.version_list_view import VersionListView


class WorkVersionsWidget(QWidget):
    h = 28
    buttons_spacing = 2
    ask_refresh_exports = Signal()

    def __init__(self, stage: Stage=None):
        super().__init__()
        self.stage = stage
        self._init_ui()
        self.connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)

        # ------------------------
        # main layout
        # ------------------------
        sub_layout = QHBoxLayout()
        layout.addLayout(sub_layout)

        # ------------------------
        # versions list
        # ------------------------
        v_layout = QVBoxLayout()
        sub_layout.addLayout(v_layout)

        # new buttons
        label = QLabel("Work versions")
        v_layout.addWidget(label)

        h_layout = QHBoxLayout()
        v_layout.addLayout(h_layout)
        h_layout.setSpacing(self.buttons_spacing)

        new_file_button = PushButtonAutoWidth(
            text=" New", icon_name='ph.selection-bold',
            tooltip="Create an empty file",
            fixed_width=True,
        )
        h_layout.addWidget(new_file_button)

        increment_button = PushButtonAutoWidth(
            text=" Increment", icon_name='fa5s.arrow-up',
            tooltip="Create a copy of the selected version",
        )
        h_layout.addWidget(increment_button)

        # versions list
        versions_list = VersionListView()
        versions_list.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        v_layout.addWidget(versions_list)

        # buttons
        h_layout = QHBoxLayout()
        v_layout.addLayout(h_layout)
        h_layout.setSpacing(self.buttons_spacing)

        turbine_button = PushButtonAutoWidth(
            text=" Turbine", icon_name='fa.gears',
            tooltip="Choose a process to launch in turbine",
        )
        h_layout.addWidget(turbine_button)

        # # ------------------------
        # # boxes
        # # ------------------------
        # v_layout = QVBoxLayout()
        # sub_layout.addLayout(v_layout)
        #
        # comment_box = TextBox(title="Comment:")
        # v_layout.addWidget(comment_box)
        #
        # todo_list = TextBox(title="To do:")
        # v_layout.addWidget(todo_list)

        # ------------------------
        # public vars
        # ------------------------
        self.new_file_button = new_file_button
        self.increment_button = increment_button
        self.turbine_button = turbine_button

        self.versions_list = versions_list

    def connect_signals(self):
        self.new_file_button.clicked.connect(self.on_new_file_button_clicked)
        self.increment_button.clicked.connect(self.on_increment_button_clicked)
        self.turbine_button.clicked.connect(self.on_turbine_button_clicked)
        self.versions_list.double_clicked.connect(self.on_version_list_double_clicked)
        self.versions_list.customContextMenuRequested.connect(self.show_context_menu)

        self.ask_refresh_exports.connect(self.refresh)

    def refresh(self):
        self.versions_list.refresh()

    def on_version_list_double_clicked(self):
        version = self.versions_list.get_hovered_version()
        file = version.to_file()
        file.open_interactive()
        print(f"Opening {version.software.label} file: {version.filepath}")

    def show_context_menu(self, position: QPoint):
        # TODO: rmb -> exit, remove close button if done
        version = self.versions_list.get_hovered_version()

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

    def on_new_file_button_clicked(self):
        if self.stage is None:
            return

        work_versions_api.new_empty_version(stage=self.stage)

        self.refresh()
        self.versions_list.select_row(0)

    def on_increment_button_clicked(self):
        if self.stage is None:
            return

        old_version = self.versions_list.get_selected_version()
        work_versions_api.increment(old_version=old_version)

        self.refresh()
        self.versions_list.select_row(0)

    def on_turbine_button_clicked(self):
        if self.stage is None:
            return
        process_select_menu = ProcessSelectMenu(component=self.stage.work_component, version=self.versions_list.get_selected_version())
        process_select_menu.process_finished.connect(self.ask_refresh_exports.emit)
        process_select_menu.process_finished.connect(self.refresh)

        confirm = process_select_menu.show_menu(position=[0.5, 1])
        print(f"{confirm = }")

    def set_stage(self, stage: Stage):
        self.stage = stage
        if stage is None:
            return

        self.versions_list.set_component(stage.work_component)
        self.versions_list.select_row(0)
