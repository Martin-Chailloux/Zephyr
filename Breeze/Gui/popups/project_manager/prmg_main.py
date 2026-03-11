import qtawesome
from PySide6.QtWidgets import QDialog, QVBoxLayout, QSplitter

from Breeze.Api.breeze_app import BreezeApp
from Breeze.Gui.popups.project_manager.prmg_project_settings import ProjectSettingsWidget
from Breeze.Gui.popups.project_manager.prmg_project_selector import ProjectSelectorWidget


class ProjectManager(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(qtawesome.icon("mdi.movie-open-cog"))
        self.setWindowTitle("Project Manager")
        self._init_ui()
        self._connect_signals()
        self._init_state()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        splitter = QSplitter()
        layout.addWidget(splitter)

        projects_selector = ProjectSelectorWidget()
        splitter.addWidget(projects_selector)

        project_settings = ProjectSettingsWidget()
        splitter.addWidget(project_settings)

        self.projects_selector = projects_selector
        self.project_settings = project_settings

    def _connect_signals(self):
        self.projects_selector.projects_list.selectionModel().selectionChanged.connect(self.on_project_selected)

    def _init_state(self):
        pass

    def on_project_selected(self):
        project = self.projects_selector.projects_list.get_project()
        BreezeApp.set_project(name=project.name)
        self.project_settings.refresh()
        self.project_settings.update()  # updates the thumbnail immediately
