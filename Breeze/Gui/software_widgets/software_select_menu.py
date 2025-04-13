from PySide6.QtWidgets import QVBoxLayout

from Data.project_documents import Stage
from Data.studio_documents import Software
from Gui.abstract_widgets.context_menu_widget import ContextMenuWidget
from Gui.software_widgets.software_list.software_list_view import SoftwareListView


class SoftwareSelectMenu(ContextMenuWidget):

    def __init__(self, stage: Stage):
        super().__init__(w=168, h=248, position=[0.5, 0])
        self.stage = stage
        self.software: Software = None  # is set when closed
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        software_list = SoftwareListView(stage=self.stage)
        layout.addWidget(software_list)
        # software_list.set_selected_user(self.stage.user)

        self.software_list = software_list

    def _connect_signals(self):
        self.software_list.software_selected.connect(self.on_software_selected)
        self.software_list.right_clicked.connect(self.close)

    def on_software_selected(self, label: str):
        software = Software.objects.get(label=label)
        self.software = software
        self.close()
