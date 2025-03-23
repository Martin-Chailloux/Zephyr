from PySide6.QtWidgets import QLineEdit


class SearchbarWidget(QLineEdit):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._set_initial_state()

    def _init_ui(self):
        self.setPlaceholderText("Search")

    def _set_initial_state(self):
        self.setMaximumWidth(172)
