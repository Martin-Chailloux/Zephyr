import qtawesome
from PySide6.QtWidgets import QVBoxLayout, QPushButton

from Data.breeze_app import BreezeApp
from Data.project_documents import Version
from Gui.GuiWidgets.abstract_widgets.context_menu_widget import ContextMenuWidget
from Gui.GuiWidgets.process_widgets.process_list.process_list_view import ProcessListView
from Turbine.tb_core import CommonProcess


class ProcessSelectMenu(ContextMenuWidget):
    project = BreezeApp.project
    users = project.users

    def __init__(self, version: Version):
        super().__init__(w=168, h=248, position=[0.5, 1])
        self.version = version
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        process_list = ProcessListView()
        layout.addWidget(process_list)
        process_list.set_stage_template(stage_template=self.version.component.stage.stage_template)

        launch_button = QPushButton("Launch")
        layout.addWidget(launch_button)
        launch_button.setIcon(qtawesome.icon('fa.rocket'))
        launch_button.setFixedHeight(32)

        self.processes_list = process_list
        self.launch_button = launch_button

    def _connect_signals(self):
        self.processes_list.process_selected.connect(self.on_process_selected)
        self.processes_list.right_clicked.connect(self.reject)
        self.launch_button.clicked.connect(self.on_launch_button_clicked)

    def on_process_selected(self, pseudo: str):
        # TODO: update ui on the right side with process infos + inputs
        pass
        # process = MgPR.objects.get(pseudo=pseudo)
        # self.accept()

    def on_launch_button_clicked(self):
        process: CommonProcess.__class__ = self.processes_list.get_selected_process()
        # TODO: fix typing
        #  - here: emit signal
        #  - add user and version in inputs
        #  - stage_template should be taken from version.collection.stage.stage_template
        process = process(user=BreezeApp.user, version=self.version)
        process.run()
        print(f"{process = }")
