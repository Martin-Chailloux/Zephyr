import sys

import qtawesome

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QMainWindow, QDockWidget
import qdarkstyle

from Data.breeze_documents import Stage
from Gui.panels.select_stage_panel import SelectStagePanel
from Gui.panels.stage_panel import StagePanel
from Utils.chronometer import Chronometer


class Breeze(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Breeze")
        self.setWindowIcon(qtawesome.icon("fa5s.wind"))
        self._init_ui()
        self.connect_signals()

    def _init_ui(self):
        # stage central widget
        stage_panel = StagePanel()
        self.setCentralWidget(stage_panel)

        # stage select
        select_stage_panel = SelectStagePanel()
        dock = QDockWidget("Select Stage")
        dock.setWidget(select_stage_panel)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, dock)
        dock.setAllowedAreas(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea)

        # public vars
        self.select_stage_panel = select_stage_panel
        self.stage_panel = stage_panel

    def connect_signals(self):
        self.select_stage_panel.stage_list_widget.stage_selected.connect(self.on_stage_selected)

    def on_stage_selected(self, longname: str):
        stage = Stage.objects.get(longname=longname)
        self.stage_panel.stage_versions_widget.stage_item.set_stage(stage=stage)


if __name__ == '__main__':
    print(f"Launching 'Breeze' ...")
    chrono = Chronometer()

    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())

    window = Breeze()
    window.show()
    print(f"... Finished launching 'Breeze' in: {chrono.tick()}")
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
        msg = f"Run time: {time: 2.2f} seconds."
    print(msg)
