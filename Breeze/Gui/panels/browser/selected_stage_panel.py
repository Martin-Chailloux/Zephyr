from typing import Optional

from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QLabel

from Api.project_documents import Stage
from Gui.panels.browser.sub_panels.stage_exports_subpanel import SelectedStageSubPanel
from Gui.panels.browser.sub_panels.work_versions_subpanel import WorkVersionsWidget
from Gui.sub_widgets.stage_widgets.stage_banner_widget import StageBannerWidget


class SelectedStagePanel(QWidget):
    stage_data_modified = Signal()

    def __init__(self):
        super().__init__()
        self._init_ui()
        self.stage: Optional[Stage] = None

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)

        # TODO [fix]: when changing asset this jumps to the last stage of the list
        stage_banner_widget = StageBannerWidget()
        layout.addWidget(stage_banner_widget)

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

    def _on_stage_data_modified(self):
        self.stage_data_modified.emit()

    def refresh(self):
        self.stage_banner_widget.stage_list.refresh()
