from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QLabel

from Gui.version_widgets.work_versions_widget import WorkVersionsWidget


class StagePanel(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        placeholder1 = QLabel()
        work_versions_widget = WorkVersionsWidget(stage=None)
        placeholder2 = QLabel()

        v_splitter = QSplitter()
        v_splitter.setOrientation(QtCore.Qt.Orientation.Vertical)
        v_splitter.setChildrenCollapsible(False)
        v_splitter.addWidget(work_versions_widget)
        v_splitter.addWidget(placeholder2)

        h_splitter = QSplitter()
        layout.addWidget(h_splitter)
        h_splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        h_splitter.setChildrenCollapsible(False)

        h_splitter.addWidget(placeholder1)
        h_splitter.addWidget(v_splitter)

        # public vars
        self.work_versions_widget = work_versions_widget
