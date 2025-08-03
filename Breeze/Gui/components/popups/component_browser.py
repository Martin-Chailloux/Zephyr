from PySide6.QtWidgets import QVBoxLayout, QTextEdit

from Gui.components.mvd.component_mvd.component_list_view import ComponentListView
from Gui.components.popups.abstract_popup_widget import AbstractPopupWidget


class ComponentBrowser(AbstractPopupWidget):

    def __init__(self):
        super().__init__(w=280, position=[0.5, 1], show_borders=True)
        self.setWindowTitle("Select a component")
        self._init_ui()
        self._connect_signals()
        self._init_state()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # TODO: subwidget
        search_bar = QTextEdit()
        layout.addWidget(search_bar)
        search_bar.setFixedHeight(32)
        search_bar.setPlaceholderText("Search")

        component_list = ComponentListView()
        layout.addWidget(component_list)

        self.search_bar = search_bar
        self.component_list = component_list

    def _connect_signals(self):
        self.search_bar.textChanged.connect(self.on_searchbar_edited)

    def on_searchbar_edited(self):
        text = self.search_bar.toPlainText().lower()
        self.component_list.set_text_filter(text=text)

    def _init_state(self):
        pass
