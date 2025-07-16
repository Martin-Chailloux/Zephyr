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

        self.exports_table = table

    def set_stage(self, stage: Stage = None):
        self.stage = stage
        self.exports_table.set_stage(stage=stage)

    def refresh(self):
        self.exports_table.refresh()


class StageExportsTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.stage: Optional[Stage] = None
        self.versions: list[Version] = []

    def populate(self, versions: list[Version]):
        self.versions = versions

        self.clear()
        if not versions:
            return

        work_component = versions[0].component.stage.work_component
        print(f"{work_component = }")
        components: list[Component] = [v.component for v in versions]
        print(f"{components = }")
        components: list[Component] = [c for c in components if c != work_component]
        print(f"{components = }")
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

    def set_stage(self, stage: Stage=None):
        self.stage = stage

        if stage is None:
            return

        versions = []
        for component in stage.components:
            versions.extend(component.versions)

        self.populate(versions=versions)

    def refresh(self):
        print(f"\nREFRESH: {self.versions = }")

        if not self.versions:
            return
        if self.stage is None:
            return

        self.blockSignals(True)
        stage = Stage.objects.get(longname=self.stage.longname)
        self.set_stage(stage)
        self.blockSignals(False)
