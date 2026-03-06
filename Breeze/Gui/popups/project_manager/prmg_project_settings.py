import qtawesome
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget, QPushButton, QHBoxLayout

from Api.breeze_app import BreezeApp
from Gui.popups.project_manager.prmg_tabs.prmg_settings_tab_general import ProjectSettingsGeneralTab
from Gui.popups.project_manager.prmg_tabs.prmg_settings_tab_users import ProjectSettingsUsersTab
from Utils.sub_widgets import Thumbnail


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

        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)

        name = QLabel("Project Name")
        h_layout.addWidget(name)
        name.setStyleSheet("background-color: transparent;")

        thumbnail = Thumbnail()
        h_layout.addWidget(thumbnail)
        thumbnail.setFixedSize(QSize(int(192/2), int(108/2)))

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

        self.name = name
        self.thumbnail = thumbnail

        self.general_tab = general_tab
        self.categories_tab = None  # todo
        self.users_tab = users_tab
        self.roles_tab = None  # todo

    def _connect_signals(self):
        pass

    def _init_state(self):
        self.refresh()

    def refresh(self):
        project = BreezeApp.project
        self.name.setText(project.name)
        self.thumbnail.set_path(path=project.thumbnail_path)
        self.users_tab.refresh()
