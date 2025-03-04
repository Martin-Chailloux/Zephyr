import sys

import qdarkstyle
import qtawesome

from PySide6 import QtCore
from PySide6.QtCore import QPoint, QSize, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLabel, QSizePolicy, QMenu, QWidget, QGridLayout)

from Data import softwares
from Data.softwares import Software
from Widgets.qwidgets_extensions import TextBox, PushButtonAutoWidth, ContextWidget

from MangoEngine.document_models import Stage

from Panels.select_stage.stage_list import StageItem
from Panels.versions_list.versions_list_view import VersionsListView


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

    def set_stage(self, longname: str):
        stage = Stage.objects.get(longname=longname)
        print(f"{stage = }")

    def connect_signals(self):
        self.from_scratch_button.clicked.connect(self.on_from_scratch_clicked)
        self.from_scratch_button.customContextMenuRequested.connect(self.on_from_scratch_clicked)

    def on_from_scratch_clicked(self):
        menu = SelectSoftwareContextWidget()
        menu.exec()


class SelectSoftwareContextWidget(ContextWidget):
    software_icons = [
        softwares.Krita(),
        softwares.Blender(),
        softwares.Maya(),
        softwares.GuerillaRender(),
        softwares.Nuke(),
    ]

    margin = 2
    button_w: int = 48
    h: int = 48

    def __init__(self):
        w = (len(self.software_icons) * self.button_w) + (2 * self.margin)
        super().__init__(w=w, h=self.h,
                         align_h=QtCore.Qt.AlignmentFlag.AlignCenter,
                         align_v=QtCore.Qt.AlignmentFlag.AlignBottom)
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(self.margin, self.margin, self.margin, self.margin)
        layout.setSpacing(2)

        for i, software in enumerate(self.software_icons):
            h = self.h - 12
            button = SoftwareButton(software=software, icon_h=h)
            layout.addWidget(button)
            button.software_selected.connect(self.on_software_selected)

    def on_software_selected(self, label: str):
        print(f"software selected: {label}")
        self.close()


class SoftwareButton(QPushButton):
    software_selected = Signal(str)

    def __init__(self, software: Software, icon_h: int=36):
        super().__init__()
        self.software = software
        self.setIcon(software.icon)
        self.setIconSize(QSize(icon_h, icon_h))

        self.setToolTip(software.label)
        self.setEnabled(self.software.is_enabled)

        self.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        self.software_selected.emit(self.software.label)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyleSheet(qdarkstyle.load_stylesheet())

    window = StageVersionsWidget()
    window.show()

    app.exec()