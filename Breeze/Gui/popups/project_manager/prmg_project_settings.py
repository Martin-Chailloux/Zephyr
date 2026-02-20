import qtawesome
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget, QPushButton

from Gui.popups.project_manager.prmg_settings_tab_general import ProjectSettingsGeneralTab
from Gui.popups.project_manager.prmg_settings_tab_users import ProjectSettingsUsersTab


class ProjectSettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._connect_signals()
        self._init_state()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(0)

        name = QLabel("Jour de Vent")
        layout.addWidget(name)
        name.setStyleSheet("background-color: transparent;")
        name = QLabel("jdv")
        layout.addWidget(name)
        name.setStyleSheet("background-color: transparent;")

        layout.addSpacing(7)

        tabs = QTabWidget()
        layout.addWidget(tabs)
        tabs.setDocumentMode(True)

        general_tab = ProjectSettingsGeneralTab()
        users_tab = ProjectSettingsUsersTab()

        tabs.addTab(general_tab, " General ")
        tabs.addTab(QWidget(), " Categories ")
        tabs.addTab(users_tab, " Users ")
        tabs.addTab(QWidget(), " Roles ")

        layout.addSpacing(5)

        open_button = QPushButton("Open Project")
        layout.addWidget(open_button)
        open_button.setIcon(qtawesome.icon('fa.folder-open'))
        open_button.setFixedHeight(32)

    def _connect_signals(self):
        pass

    def _init_state(self):
        pass
