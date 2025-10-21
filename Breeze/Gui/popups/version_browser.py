from PySide6.QtWidgets import QVBoxLayout, QTextEdit, QCheckBox

from Api.document_models.project_documents import Component, Version
from Gui.mvd.component_mvd.component_list_view import ComponentListView
from Gui.mvd.version_mvd.version_list_view import VersionListView
from Gui.popups.abstract_popup_widget import AbstractPopupWidget


class VersionBrowser(AbstractPopupWidget):
    # TODO: shortcut to select the last/head version

    def __init__(self, versions: list[Version]):
        super().__init__(w=280, show_borders=True)
        self.versions = versions

        self.setWindowTitle("Select a version")
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(0)

        search_bar = QTextEdit()
        layout.addWidget(search_bar)
        search_bar.setFixedHeight(32)
        search_bar.setPlaceholderText("Search")

        layout.addSpacing(12)

        version_list = VersionListView()
        layout.addWidget(version_list)
        version_list.set_versions(versions=self.versions)

        self.search_bar = search_bar
        self.versions_list = version_list

    def _connect_signals(self):
        self.search_bar.textChanged.connect(self.on_searchbar_edited)
        self.versions_list.right_clicked.connect(self.reject)
        self.versions_list.selectionModel().selectionChanged.connect(self.accept)

    def on_searchbar_edited(self):
        text = self.search_bar.toPlainText().lower()
        self.versions_list.set_text_filter(text=text)
