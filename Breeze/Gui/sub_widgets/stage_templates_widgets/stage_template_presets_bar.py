from PySide6 import QtCore
from PySide6.QtWidgets import QVBoxLayout, QWidget, QComboBox, QHBoxLayout, QLabel

from Gui.sub_widgets.util_widgets.util_widgets import IconButton


class StageTemplatesPresetsBar(QWidget):
    wh = 28

    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(3)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)

        # label
        label = QLabel("Preset")
        layout.addWidget(label)

        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)

        combobox = QComboBox()
        h_layout.addWidget(combobox)

        save_button = IconButton(icon_name="mdi6.content-save", width=self.wh)
        h_layout.addWidget(save_button)
        save_button.setToolTip("Save preset")

        save_as_button = IconButton(icon_name="mdi6.content-save-plus", width=self.wh)
        h_layout.addWidget(save_as_button)
        save_as_button.setToolTip("Save as new preset")

        self.combobox = combobox
        self.save_button = save_button
        self.save_as_button = save_as_button
