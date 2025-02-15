from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QPushButton, QLabel

from Panels.select_stage_version.select_stage_version_widget import SelectStageVersionWidget


class StagePanel(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        placeholder1 = QLabel()
        select_stage_version = SelectStageVersionWidget()
        placeholder2 = QLabel()

        v_splitter = QSplitter()
        v_splitter.setOrientation(QtCore.Qt.Orientation.Vertical)
        v_splitter.setChildrenCollapsible(False)
        v_splitter.addWidget(select_stage_version)
        v_splitter.addWidget(placeholder2)

        h_splitter = QSplitter()
        layout.addWidget(h_splitter)
        h_splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        h_splitter.setChildrenCollapsible(False)

        h_splitter.addWidget(placeholder1)
        h_splitter.addWidget(v_splitter)
