from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                               QLabel, QSizePolicy)

from Data.project_documents import Stage
from Gui.GuiWidgets.process_widgets.process_launcher import ProcessSelectMenu
from Gui.GuiWidgets.stages_widgets.stage_list.stage_list_item_delegate import StageListItemAlwaysOnDelegate
from Gui.GuiWidgets.stages_widgets.stage_list.stage_list_model import StageItemMetrics
from Gui.GuiWidgets.stages_widgets.stage_list.stage_list_view import StageListView
from Gui.GuiWidgets.util_widgets.util_widgets import TextBox, PushButtonAutoWidth
from Gui.GuiWidgets.version_widgets import work_versions_api
from Gui.GuiWidgets.version_widgets.versions_list.versions_list_view import VersionListView


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
        self._asset_label = asset_label

        self.new_file_button = new_file_button
        self.increment_button = increment_button
        self.turbine_button = turbine_button

        self.stage_list_view = stage_list_view

        self.versions_list = versions_list

    def connect_signals(self):
        self.new_file_button.clicked.connect(self.on_new_file_button_clicked)
        self.increment_button.clicked.connect(self.on_increment_button_clicked)
        self.turbine_button.clicked.connect(self.on_turbine_button_clicked)

    def on_new_file_button_clicked(self):
        if self.stage is None:
            return

        work_versions_api.new_empty_version(stage=self.stage)

        self.versions_list.refresh()
        self.versions_list.select_row(0)

    def on_increment_button_clicked(self):
        if self.stage is None:
            return

        old_version = self.versions_list.get_selected_version()
        work_versions_api.increment(old_version=old_version)

        self.versions_list.refresh()
        self.versions_list.select_row(0)

    def on_turbine_button_clicked(self):
        if self.stage is None:
            return
        menu = ProcessSelectMenu(version=self.versions_list.get_selected_version())
        confirm = menu.exec()
        print(f"{confirm = }")

    def set_stage(self, stage: Stage):
        self.stage = stage
        self.stage_list_view.set_stage(stage)

        if stage is None:
            text = ""
        else:
            text = f"{stage.asset.category} > {stage.asset.name} > {stage.asset.variant}"
        self._asset_label.setText(text)

        self.versions_list.set_collection(stage.work_collection)
        self.versions_list.select_row(0)
