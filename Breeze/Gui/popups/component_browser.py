from PySide6.QtWidgets import QVBoxLayout, QTextEdit, QCheckBox

from Api.document_models.project_documents import Component, Stage
from Gui.mvd.component_mvd.component_list_view import ComponentListView
from Gui.popups.abstract_popup_widget import AbstractPopupWidget


class ComponentBrowser(AbstractPopupWidget):
    def __init__(self, components: list[Component], stage: Stage):
        super().__init__(w=280, show_borders=True)
        components = [x for x in components if x.get_last_version() is not None]  # dont add components without version
        self.components = components
        self.stage = stage
        self.stage_components = [c for c in components if c.stage == self.stage]

        self.text_filter: str = ""  # needed to refresh after all stages checkbox has been clicked

        self.setWindowTitle("Select a component")
        self._init_ui()
        self._connect_signals()
        self._init_state()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(0)

        search_bar = QTextEdit()
        layout.addWidget(search_bar)
        search_bar.setFixedHeight(32)
        search_bar.setPlaceholderText("Search")

        layout.addSpacing(12)

        show_all_stages_checkbox = QCheckBox("Show all stages")
        layout.addWidget(show_all_stages_checkbox)

        component_list = ComponentListView()
        layout.addWidget(component_list)
        component_list.set_components(components=self.components, filtered_components=self.stage_components)

        self.search_bar = search_bar
        self.show_all_stages_checkbox = show_all_stages_checkbox
        self.component_list = component_list

    def _connect_signals(self):
        self.search_bar.textChanged.connect(self.on_searchbar_edited)
        self.show_all_stages_checkbox.clicked.connect(self.on_show_all_stages_checkbox_clicked)
        self.component_list.right_clicked.connect(self.reject)
        self.component_list.selectionModel().selectionChanged.connect(self.accept)

    def _init_state(self):
        self.component_list.set_text_filter(text=self.text_filter)

    def on_searchbar_edited(self):
        text = self.search_bar.toPlainText().lower()
        self.component_list.set_text_filter(text=text)
        self.text_filter = text

    def on_show_all_stages_checkbox_clicked(self, is_checked: bool):
        self.component_list.set_only_show_filtered_components(show=not is_checked)
        self.component_list.set_text_filter(text=self.text_filter)
