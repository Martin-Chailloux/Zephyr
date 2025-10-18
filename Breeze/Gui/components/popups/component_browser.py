from PySide6.QtWidgets import QVBoxLayout, QTextEdit, QCheckBox

from Api.project_documents import Component
from Gui.components.mvd.component_mvd.component_list_view import ComponentListView
from Gui.components.popups.abstract_popup_widget import AbstractPopupWidget


class ComponentBrowser(AbstractPopupWidget):
    def __init__(self, components: list[Component]):
        super().__init__(w=280, show_borders=True)
        components = [x for x in components if x.get_last_version() is not None]  # dont add components without version
        self.components = components

        self.setWindowTitle("Select a component")
        self._init_ui()
        self._connect_signals()
        self._init_state()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(0)

        # TODO: subwidget
        search_bar = QTextEdit()
        layout.addWidget(search_bar)
        search_bar.setFixedHeight(32)
        search_bar.setPlaceholderText("Search")

        layout.addSpacing(12)

        show_more_checkbox = QCheckBox("Show all stages")
        layout.addWidget(show_more_checkbox)

        component_list = ComponentListView()
        layout.addWidget(component_list)
        component_list.set_components(components=self.components)

        self.search_bar = search_bar
        self.component_list = component_list

    def _connect_signals(self):
        self.search_bar.textChanged.connect(self.on_searchbar_edited)
        self.component_list.right_clicked.connect(self.reject)
        self.component_list.component_selected.connect(self.on_component_selected)

    def on_searchbar_edited(self):
        text = self.search_bar.toPlainText().lower()
        self.component_list.set_text_filter(text=text)

    def on_component_selected(self):
        component = self.component_list.get_selected_component()
        print(f"1, {component = }")
        self.close()

    def _init_state(self):
        pass
