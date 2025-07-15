from multiprocessing.util import sub_debug
from typing import Optional

import qtawesome
from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QLabel, QHBoxLayout, QPushButton

from Api.breeze_app import BreezeApp
from Api.project_documents import Stage
from Gui.panels.browser.sub_panels.stage_exports_subpanel import SelectedStageSubPanel
from Gui.panels.browser.sub_panels.work_versions_subpanel import WorkVersionsWidget
from Gui.sub_widgets.stage_widgets.stage_banner_widget import StageBannerWidget
from Gui.sub_widgets.util_widgets.util_widgets import IconButton, IconLabel


class SelectedStagePanel(QWidget):
    stage_data_modified = Signal()

    def __init__(self):
        super().__init__()
        self._init_ui()
        self._connect_signals()
        self.stage: Optional[Stage] = None

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)

        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)

        # ------------------------
        # Upper banner
        # ------------------------

        # banner
        stage_banner_widget = StageBannerWidget()
        h_layout.addWidget(stage_banner_widget)

        # splitter visibility controls
        sub_layout = QHBoxLayout()
        h_layout.addLayout(sub_layout)
        sub_layout.setSpacing(1)
        sub_layout.setContentsMargins(0, 0, 0, 0)

        button_l = QPushButton()
        button_m = QPushButton()
        button_r = QPushButton()
        for button in [button_l, button_m, button_r]:
            sub_layout.addWidget(button)
            button.setCheckable(True)
            button.setChecked(True)
            button.setFixedSize(36, 36)

            color = BreezeApp.palette.green
            stylesheet = f"QPushButton:checked {{background-color: {color}}};"
            button.setStyleSheet(stylesheet)

        # ------------------------
        # splitter
        # ------------------------
        placeholder1 = QLabel()
        work_versions_widget = WorkVersionsWidget(stage=None)
        stage_exports_widget = SelectedStageSubPanel()

        v_splitter = QSplitter()
        layout.addWidget(v_splitter, 1)
        v_splitter.setChildrenCollapsible(False)
        v_splitter.addWidget(placeholder1)
        v_splitter.addWidget(work_versions_widget)
        v_splitter.addWidget(stage_exports_widget)

        layout.setStretch(0, 0)

        # public vars
        self.stage_banner_widget = stage_banner_widget
        self.button_l = button_l
        self.button_m = button_m
        self.button_r = button_r

        self.placeholder1 = placeholder1
        self.work_versions_widget = work_versions_widget
        self.stage_exports_widget = stage_exports_widget

    def set_stage(self, stage: Stage = None):
        self.stage = stage
        self.stage_banner_widget.set_stage(stage=stage)
        self.work_versions_widget.set_stage(stage=stage)
        self.stage_exports_widget.set_stage(stage=stage)

    def _connect_signals(self):
        # promote from sub-widgets
        self.stage_banner_widget.stage_list.stage_data_modified.connect(self._on_stage_data_modified)
        self.button_l.clicked.connect(self._on_splitter_button_clicked)
        self.button_m.clicked.connect(self._on_splitter_button_clicked)
        self.button_r.clicked.connect(self._on_splitter_button_clicked)

    def _on_stage_data_modified(self):
        self.stage_data_modified.emit()

    def refresh(self):
        self.stage_banner_widget.stage_list.refresh()

    def _on_splitter_button_clicked(self, is_checked: bool):
        """ shows or hides the matching widget """
        # TODO: don't allow to hide everything
        #  autoresize: bool -> external setting
        #  isolate the 3 buttons into their own widget
        button : QPushButton = self.sender()
        if button is self.button_l:
            self.placeholder1.setVisible(is_checked)
        elif button is self.button_m:
            self.work_versions_widget.setVisible(is_checked)
        elif button is self.button_r:
            self.stage_exports_widget.setVisible(is_checked)
