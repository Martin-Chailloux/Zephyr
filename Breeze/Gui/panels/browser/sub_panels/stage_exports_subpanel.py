from typing import Optional

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel

from Api.project_documents import Stage, Component, Version


class SelectedStageSubPanel(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self.stage: Optional[Stage] = None

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("Exports")
        layout.addWidget(title)

        table = StageExportsTable()
        layout.addWidget(table)

        self.table = table

    def set_stage(self, stage: Stage = None):
        self.stage = stage
        if stage is None:
            return

        versions = []
        for component in stage.components:
            versions.extend(component.versions)

        self.table.populate(versions=versions)


class StageExportsTable(QTableWidget):
    def populate(self, versions: list[Version]):
        self.clear()
        if not versions:
            return

        work_component = versions[0].component.stage.work_component
        components: list[Component] = [v.component for v in versions if v.component != work_component]
        components = list(set(components))
        self.setColumnCount(len(components))
        self.setHorizontalHeaderLabels([c.label for c in components])
        columns = {component.label: i for i, component in enumerate(components)}

        numbers: list[int] = [v.number for v in versions]
        numbers = list(set(numbers))
        numbers.reverse()
        self.setRowCount(len(numbers))
        self.setVerticalHeaderLabels([f"{n:03d}" for n in numbers])
        rows = {f"{number:03d}": i for i, number in enumerate(numbers)}

        for version in versions:
            row = rows.get(f"{version.number:03d}", None)
            column = columns.get(version.component.label, None)

            if row is not None and column is not None:
                text = f".{version.software.extension}"
                item = QTableWidgetItem(text)
                self.setItem(row, column, item)
