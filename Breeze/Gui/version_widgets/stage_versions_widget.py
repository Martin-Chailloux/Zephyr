import sys

import qdarkstyle

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout,
                               QLabel, QSizePolicy)

from Data.software_model import SoftwareModel
from Data.breeze_documents import Stage
from Gui.stage_widgets.stage_item import StageItem
from Gui.popups.select_software_popup import SelectSoftwarePopup
from Gui.version_widgets.versions_list.versions_list_view import VersionsListView
from Gui.util_widgets.util_widgets import TextBox, PushButtonAutoWidth


class StageVersionsWidget(QDialog):
    h = 28
    buttons_spacing = 2

    def __init__(self):
        super().__init__()
        self._init_ui()
        self.connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # ------------------------
        # header
        # ------------------------
        sub_layout = QHBoxLayout()
        layout.addLayout(sub_layout)
        sub_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        label = QLabel("Selected stage:")
        sub_layout.addWidget(label)
        label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        stage_item = StageItem(stage=Stage.objects[0])
        sub_layout.addWidget(stage_item)
        stage_item.setFixedWidth(248)

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

        v_layout.addSpacing(28)

        # new buttons
        label = QLabel("Create new version:")
        v_layout.addWidget(label)

        h_layout = QHBoxLayout()
        v_layout.addLayout(h_layout)
        h_layout.setSpacing(self.buttons_spacing)

        from_scratch_button = PushButtonAutoWidth(
            text=" Empty", icon_name='ph.selection-bold',
            tooltip="use an empty file",
            fixed_width=True,
        )
        h_layout.addWidget(from_scratch_button)

        increment_button = PushButtonAutoWidth(
            text=" Increment", icon_name='fa5s.arrow-up',
            tooltip="use a copy of the selected version",
        )
        h_layout.addWidget(increment_button)

        # versions list
        versions_list = VersionsListView()
        v_layout.addWidget(versions_list)
        for i in range(51, 0, -1):
            versions_list.add_version(i)

        # buttons
        h_layout = QHBoxLayout()
        v_layout.addLayout(h_layout)
        h_layout.setSpacing(self.buttons_spacing)

        processes_button = PushButtonAutoWidth(
            text=" Processes", icon_name='fa.gears',
            tooltip="Choose a process to launch",
            fixed_width=True,
        )
        h_layout.addWidget(processes_button)

        launch_button = PushButtonAutoWidth(
            text=" Launch", icon_name='fa5s.rocket',
            tooltip="Open the selected file within its software",
        )
        h_layout.addWidget(launch_button)

        # TODO: open_folder & copy_path in a context menu
        # open_folder_button = IconButton(icon_name="fa5s.folder-open")
        # h_layout.addWidget(open_folder_button)
        # open_folder_button.setToolTip("Open folder")
        #
        # copy_path_button = IconButton(icon_name="fa5s.copy")
        # h_layout.addWidget(copy_path_button)
        # copy_path_button.setToolTip("Copy path")

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
        self.from_scratch_button = from_scratch_button
        self.stage_item = stage_item

    def connect_signals(self):
        self.from_scratch_button.clicked.connect(self.on_from_scratch_clicked)
        self.from_scratch_button.customContextMenuRequested.connect(self.on_from_scratch_clicked)

    def on_from_scratch_clicked(self):
        dialog = SelectSoftwarePopup(
            available_soft= [
                SoftwareModel.krita,
                SoftwareModel.maya,
                SoftwareModel.blender,
                SoftwareModel.guerilla,
                SoftwareModel.nuke,
            ],
            recommended_soft= [
                SoftwareModel.blender,
                SoftwareModel.nuke,
            ],
        )

        dialog.resize(QSize(420, 360))
        dialog.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyleSheet(qdarkstyle.load_stylesheet())

    window = StageVersionsWidget()
    window.show()

    app.exec()