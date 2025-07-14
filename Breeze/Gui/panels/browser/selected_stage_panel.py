from typing import Optional

from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QLabel

from Api.project_documents import Stage
from Gui.panels.browser.work_versions.work_versions_subpanel import WorkVersionsWidget
from Gui.sub_widgets.stage_widgets.stage_banner_widget import StageBannerWidget


class SelectedStagePanel(QWidget):
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
        placeholder2 = QLabel()

        v_splitter = QSplitter()
        layout.addWidget(v_splitter, 1)
        v_splitter.setChildrenCollapsible(False)
        v_splitter.addWidget(placeholder1)
        v_splitter.addWidget(work_versions_widget)
        v_splitter.addWidget(placeholder2)

        layout.setStretch(0, 0)

        # public vars
        self.stage_banner_widget = stage_banner_widget
        self.work_versions_widget = work_versions_widget

    def set_stage(self, stage: Stage = None):
        self.stage = stage
        self.stage_banner_widget.set_stage(stage=stage)
        self.work_versions_widget.set_stage(stage=stage)

