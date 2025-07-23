from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QWidget

from Api.project_documents import Stage
from Gui.components.popups.process_launcher import ProcessSelectMenu
from Gui.sub_widgets.util_widgets.util_widgets import TextBox, PushButtonAutoWidth, IconButton
from Gui.panels.browser.sub_panels import work_versions_api
from Gui.components.mvd.version_mvd.version_list_view import VersionListView


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
        v_layout.addWidget(versions_list)

        # buttons
        h_layout = QHBoxLayout()
        v_layout.addLayout(h_layout)
        h_layout.setSpacing(self.buttons_spacing)

        turbine_button = PushButtonAutoWidth(
            text=" Turbine", icon_name='fa.gears',
            tooltip="Choose a process to launch in turbine",
            fixed_width=True,
        )
        h_layout.addWidget(turbine_button)

        launch_button = PushButtonAutoWidth(
            text=" Launch", icon_name='fa5s.rocket',
            tooltip="Open the selected file within its software",
        )
        h_layout.addWidget(launch_button)

        # ------------------------
        # boxes
        # ------------------------
        v_layout = QVBoxLayout()
        sub_layout.addLayout(v_layout)

        comment_box = TextBox(title="Comment:")
        v_layout.addWidget(comment_box)

        todo_list = TextBox(title="To do:")
        v_layout.addWidget(todo_list)

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

        self.ask_refresh_exports.connect(self.refresh)

    def refresh(self):
        self.versions_list.refresh()

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
        menu = ProcessSelectMenu(component=self.stage.work_component, version=self.versions_list.get_selected_version())
        menu.process_finished.connect(self.ask_refresh_exports.emit)
        menu.process_finished.connect(self.refresh)

        confirm = menu.exec()
        print(f"{confirm = }")

    def set_stage(self, stage: Stage):
        self.stage = stage
        if stage is None:
            return

        self.versions_list.set_collection(stage.work_component)
        self.versions_list.select_row(0)
