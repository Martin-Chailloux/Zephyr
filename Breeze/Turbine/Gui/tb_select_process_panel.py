from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListView, QFormLayout, QLabel, QComboBox, QTextEdit, QHBoxLayout, \
    QFrame, QSizePolicy, QListWidget, QCheckBox, QPushButton

from Gui.GuiWidgets.util_widgets.util_widgets import IconButton
from Turbine.Gui.jobs_list.jobs_list_view import JobsListView


class SelectProcessPanel(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        # layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)

        refresh_button = IconButton(icon_name='fa.refresh')
        layout.addWidget(refresh_button)

        sub_layout = QHBoxLayout()
        layout.addLayout(sub_layout)

        user_picture = QLabel()
        sub_layout.addWidget(user_picture)
        user_picture.setFixedSize(QSize(36, 36))

        time_combobox = QComboBox()
        sub_layout.addWidget(time_combobox)
        time_combobox.addItems(["Today", "Yesterday", "Last 7 days", "Last 30 days", "All"])

        search_bar = QTextEdit()
        layout.addWidget(search_bar)
        search_bar.setFixedHeight(32)
        search_bar.setPlaceholderText("Search")

        layout.addSpacing(12)

        jobs_list = JobsListView()
        layout.addWidget(jobs_list)
        jobs_list.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        jobs_list.get_jobs()

        self.refresh_button = refresh_button
        self.jobs_list = jobs_list

    def _connect_signals(self):
        self.refresh_button.clicked.connect(self.refresh)

    def refresh(self):
        self.jobs_list.get_jobs()