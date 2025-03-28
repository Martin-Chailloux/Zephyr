import sys
from datetime import timedelta

from Utils.chronometer import Chronometer
import mongoengine

chrono = Chronometer()
print("Connecting ...")
mongoengine.connect(host="mongodb://localhost:27017/JourDeVent")
chrono.tick("... Connected in:")


import qtawesome
import qdarkstyle

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QMainWindow, QDockWidget

from Data.breeze_documents import Stage
from Gui.panels.select_stage_panel import SelectStagePanel
from Gui.panels.stage_panel import StagePanel


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

    runtime = chrono.tick()
    runtime = str(timedelta(seconds=runtime))
    hours = int(runtime.split(":")[0])
    minutes = int(runtime.split(":")[1])
    seconds = float(runtime.split(":")[2])
    msg = f"Run time: {hours}h, {minutes}m, {seconds:2.2f}s"
    print(msg)
