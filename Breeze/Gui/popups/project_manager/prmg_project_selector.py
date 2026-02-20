from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem


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

        projects_list = QListWidget()
        layout.addWidget(projects_list)

        self.projects_list = projects_list

    def _connect_signals(self):
        pass

    def _init_state(self):
        self.projects_list.addItem(QListWidgetItem("Project A"))
        self.projects_list.addItem(QListWidgetItem("Project B"))
