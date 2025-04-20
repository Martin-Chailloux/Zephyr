import sys
from datetime import timedelta

from Gui.GuiPanels.top_menu_bar import TopMenuBar
from Utils.chronometer import Chronometer
import mongoengine

import qtawesome
import qdarkstyle

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QMainWindow, QDockWidget, QMenu, QMenuBar


class BreezeMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Breeze")
        self.setWindowIcon(qtawesome.icon("fa5s.wind"))
        self._init_ui()
        self.connect_signals()

    def _init_ui(self):
        # top menu bar
        self.setMenuBar(TopMenuBar())

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
        self.select_stage_panel.stage_list_widget.stage_list_view.stage_selected.connect(self.on_stage_selected)

        self.select_stage_panel.stage_list_widget.stage_list_view.stage_data_modified.connect(self.refresh_versions_stage)
        self.stage_panel.work_versions_widget.stage_list_view.stage_data_modified.connect(self.refresh_stage_list)

    def on_stage_selected(self, longname: str):
        if longname == "":
            self.stage_panel.work_versions_widget.stage_list_view.set_stage(stage=None)
        else:
            stage = Stage.objects.get(longname=longname)
            self.stage_panel.work_versions_widget.set_stage(stage=stage)

    def refresh_stage_list(self):
        self.select_stage_panel.stage_list_widget.stage_list_view.refresh()

    def refresh_versions_stage(self):
        self.stage_panel.work_versions_widget.stage_list_view.refresh()


if __name__ == '__main__':
    print(f"Launching 'Breeze' ...")
    chrono = Chronometer()

    print("Connecting ...")
    mongoengine.connect(host="mongodb://localhost:27017", db="Studio", alias="default")

    from Data.breeze_app import BreezeApp

    app = QApplication(sys.argv)
    BreezeApp.set_project("dev")
    BreezeApp.set_user("Martin")
    app.setStyleSheet(qdarkstyle.load_stylesheet())

    mongoengine.connect(host="mongodb://localhost:27017", db=BreezeApp.project.db_name, alias="current_project")
    chrono.tick("... Connected in:")

    from Data.project_documents import Stage
    from Gui.GuiPanels.select_stage_panel import SelectStagePanel
    from Gui.GuiPanels.stage_panel import StagePanel

    window = BreezeMainWindow()
    window.show()
    chrono.tick(f"... Finished launching 'Breeze' in:")
    print("-----------------")

    app.exec()

    runtime = chrono.tick()
    runtime = str(timedelta(seconds=runtime))
    hours = int(runtime.split(":")[0])
    minutes = int(runtime.split(":")[1])
    seconds = float(runtime.split(":")[2])
    msg = f"Run time: {hours}h, {minutes}m, {seconds:2.2f}s"
    print(msg)
