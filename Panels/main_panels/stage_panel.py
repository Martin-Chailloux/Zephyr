from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QLabel

from Panels.select_stage_version.stage_versions_widget import StageVersionsWidget


class StagePanel(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        placeholder1 = QLabel()
        stage_versions_widget = StageVersionsWidget()
        placeholder2 = QLabel()

        v_splitter = QSplitter()
        v_splitter.setOrientation(QtCore.Qt.Orientation.Vertical)
        v_splitter.setChildrenCollapsible(False)
        v_splitter.addWidget(stage_versions_widget)
        v_splitter.addWidget(placeholder2)

        h_splitter = QSplitter()
        layout.addWidget(h_splitter)
        h_splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        h_splitter.setChildrenCollapsible(False)

        h_splitter.addWidget(placeholder1)
        h_splitter.addWidget(v_splitter)

        # public vars
        self.stage_versions_widget = stage_versions_widget
