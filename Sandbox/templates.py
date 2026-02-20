from PySide6.QtWidgets import QWidget, QVBoxLayout


class NewWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._connect_signals()
        self._init_state()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        # layout.setSpacing(3)
        # layout.setContentsMargins(0, 0, 0, 0)

    def _connect_signals(self):
        pass

    def _init_state(self):
        pass
