import sys
from PySide6 import QtCore
from PySide6.QtWidgets import QVBoxLayout, QDialog, QApplication, QMainWindow, QDockWidget
import qdarkstyle

from MangoEngine import project_dialog
from MangoEngine.document_models import Project
from Panels.select_stage.select_asset_widget import ZSelectAssetWidget
from Utils.chronometer import Chronometer

from Sandbox.fake_ingest_widget import ZFakeIngestWidget


class Ghost(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zephyr")

        self.setCentralWidget(TestWidget())

        project: Project = project_dialog.get_project("Dev")

        self.select_stage_widget = ZSelectAssetWidget(project)
        dock = QDockWidget("Select Stage")
        dock.setWidget(self.select_stage_widget)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, dock)
        dock.setAllowedAreas(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea)


class TestWidget(QDialog):
    def __init__(self):
        super().__init__(parent=None)
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("Zephyr")
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        fake_ingest_widget = ZFakeIngestWidget()
        layout.addWidget(fake_ingest_widget)


if __name__ == '__main__':
    chrono = Chronometer()

    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())

    window = Ghost()
    window.show()
    chrono.tick("App launched in")
    print("-----------------")

    app.exec()

    time = chrono.tick(as_float=True)
    if time > 60 * 60:
        hours = time / 60
        minutes = hours / 60
        # hours / minutes lack precision
        msg = f"Run time: {round(hours)} hours, {round(minutes)} minutes, {time % 60} seconds."
    elif time > 60:
        minutes = time / 60
        msg = f"Run time: {round(minutes)} minutes, {time % 60} seconds."
    else:
        msg = f"Run time: {time} seconds."
    print(msg)

