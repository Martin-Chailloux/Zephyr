from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                               QLabel, QSizePolicy)

from Data.converters import software_from_label
from Data.project_documents import Stage
from Gui.GuiWidgets.stages_widgets.stage_list.stage_list_item_delegate import StageListItemAlwaysOnDelegate
from Gui.GuiWidgets.stages_widgets.stage_list.stage_list_model import StageItemMetrics
from Gui.GuiWidgets.stages_widgets.stage_list.stage_list_view import StageListView
from Gui.GuiWidgets.util_widgets.util_widgets import TextBox, PushButtonAutoWidth
from Gui.GuiWidgets.version_widgets.versions_list.versions_list_view import VersionListView
from Gui.GuiWidgets.software_widgets.software_select_menu import SoftwareSelectMenu


class WorkVersionsWidget(QDialog):
    h = 28
    buttons_spacing = 2

    def __init__(self, stage: Stage):
        super().__init__()
        self.stage = stage
        self._init_ui()
        self.connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        sub_layout = QVBoxLayout()
        layout.addLayout(sub_layout)
        sub_layout.setContentsMargins(0, 0, 0, 0)
        sub_layout.setSpacing(0)

        # ------------------------
        # current asset
        # ------------------------
        asset_label = QLabel()
        sub_layout.addWidget(asset_label)
        asset_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # ------------------------
        # current stage
        # ------------------------
        # TODO: si on update la data ça reload avec l'asset entier, avec un look de spinbox
        #  C'est joli est pratique, donc:
        #  Relier la selection du stage avec ce scroll
        # TODO: cette info concerne toute la fenetre et pas que ce panel, donc faire une status bar au-dessus de l'ensemble plutôt
        stage_list_view = StageListView()
        sub_layout.addWidget(stage_list_view)
        stage_list_view.setFixedWidth(256)
        stage_list_view.setFixedSize(QSize(256, StageItemMetrics.height + 6))
        stage_list_view.setItemDelegate(StageListItemAlwaysOnDelegate())

        # ------------------------
        # main layout
        # ------------------------
        layout.addSpacing(12)

        sub_layout = QHBoxLayout()
        layout.addLayout(sub_layout)

        # ------------------------
        # versions list
        # ------------------------
        v_layout = QVBoxLayout()
        sub_layout.addLayout(v_layout)

        # new buttons
        label = QLabel("Create new version:")
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

        # TODO: par defaut selectionner la version la plus récente
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
        self.new_file_button = new_file_button
        self.stage_list_view = stage_list_view
        self._asset_label = asset_label
        self.versions_list = versions_list

    def connect_signals(self):
        self.new_file_button.clicked.connect(self.on_new_file_button_clicked)
        self.new_file_button.customContextMenuRequested.connect(self.on_new_file_button_clicked)

    def on_new_file_button_clicked(self):
        if self.stage is None:
            return

        dialog = SoftwareSelectMenu(stage=self.stage)
        dialog.exec()
        if dialog.is_canceled:
            return

        software = dialog.software
        comment = dialog.comment
        if software is None:
            return

        version = self.stage.work_collection.create_last_version(dialog.software)
        version.update(comment=comment)
        self.versions_list.refresh()

        if software.label not in software_from_label:
            raise NotImplementedError(f"Creation of a {software.label} file.")
        software = software_from_label[software.label]
        software_file = software(filepath=version.filepath)
        software_file.new_file()
        print(f"Created file: {software_file.filepath}")

    def set_stage(self, stage: Stage):
        self.stage = stage
        self.stage_list_view.set_stage(stage)

        if stage is None:
            text = ""
        else:
            text = f"{stage.asset.category} > {stage.asset.name} > {stage.asset.variant}"
        self._asset_label.setText(text)

        self.versions_list.set_collection(stage.work_collection)
