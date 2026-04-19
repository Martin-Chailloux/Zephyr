from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit

from Breeze.Gui.mvd.project_mvd.project_list_view import ProjectListView


class ProjectSelectorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._connect_signals()
        self._init_state()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        search_bar = QLineEdit()
        search_bar.setPlaceholderText("search")
        layout.addWidget(search_bar)

        projects_list = ProjectListView()
        projects_list.set_projects()
        layout.addWidget(projects_list)

        self.projects_list = projects_list

    def _connect_signals(self):
        pass

    def _init_state(self):
        pass
