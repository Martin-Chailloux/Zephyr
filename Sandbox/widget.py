import sys

import mongoengine
import qdarkstyle
from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout

mongoengine.connect(host="mongodb://localhost:27017", db="Studio", alias="default")

from Api.breeze_app import BreezeApp
from Api.project_documents import Component
from Gui.components.mvd.component_mvd.component_list_view import ComponentListView

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

        subwidget = ComponentListView()
        layout.addWidget(subwidget)

        components = Component.objects()
        subwidget.set_components(components=components)

    def _connect_signals(self):
        pass

    def _init_state(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())

    BreezeApp.set_project("JourDeVent")
    BreezeApp.set_user("Martin")
    print(f"{BreezeApp.palette = }")

    widget = Widget()
    widget.show()

    app.exec()
