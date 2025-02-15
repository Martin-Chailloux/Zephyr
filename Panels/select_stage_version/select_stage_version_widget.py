import sys

import qdarkstyle
import qtawesome

from PySide6 import QtCore
from PySide6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLabel, QSizePolicy)
from Widgets.qwidgets_extensions import TextBox, PushButtonAutoWidth

from MangoEngine.document_models import Stage

from Panels.select_stage.stage_list import StageItem
from Panels.versions_list.versions_list_view import VersionsListView


class SelectStageVersionWidget(QDialog):
    h = 28
    buttons_spacing = 2

    def __init__(self):
        super().__init__()
        self._init_ui()

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

        # TODO: update using a signal from stage select
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
            text=" From scratch", icon_name='ph.selection-bold',
            tooltip="use an empty file",
            fixed_width=True,
        )
        h_layout.addWidget(from_scratch_button)

        from_scratch_button = PushButtonAutoWidth(
            text=" Increment", icon_name='fa5s.arrow-up',
            tooltip="use a copy of the selected version",
        )
        h_layout.addWidget(from_scratch_button)

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



if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyleSheet(qdarkstyle.load_stylesheet())

    window = SelectStageVersionWidget()
    window.show()

    app.exec()