import sys

import logging
from io import StringIO

import mongoengine
import qdarkstyle
from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QTextEdit

from Api.turbine.inputs_ui import ProcessInputsUi

mongoengine.connect(host="mongodb://localhost:27017", db="Studio", alias="default")
from Processes.blender.modeling.export.ui import BlenderModelingExportUi

mongoengine.connect(host="mongodb://localhost:27017", db="JourDeVent", alias="current_project")


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._connect_signals()
        self._init_state()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        subwidget = ProcessInputsUi()
        layout.addWidget(subwidget)

        allow_overwrite = subwidget.add_checkbox(name='allow_overwrite', label='Allow overwrite', value=False)
        last_version = subwidget.add_checkbox(name='last_version', label='Last version', value=True)

        items = [f"{i:03d}" for i in range(12, 0, -1)]
        version_number = subwidget.add_combobox(name='version_num', label='Version num', items=items, value='009')
        version_number.setFixedWidth(64)

        self.process_inputs = subwidget
        self.allow_overwrite = allow_overwrite
        self.last_version = last_version
        self.version_number = version_number

    def _connect_signals(self):
        self.last_version.clicked.connect(self.on_last_version_clicked)

    def on_last_version_clicked(self, is_checked: bool):
        self.version_number.setEnabled(not is_checked)

    def _init_state(self):
        self.on_last_version_clicked(is_checked=self.last_version.isChecked())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())

    widget = Widget()
    widget.show()

    print(f"{widget.process_inputs.to_dict() = }")

    app.exec()
