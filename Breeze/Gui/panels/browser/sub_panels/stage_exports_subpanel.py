from typing import Optional

import qtawesome
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel

from Api.document_models.project_documents import Stage, Component, Version
from Utils.sub_widgets import IconLabel


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

        # columns (components)
        components: list[Component] = [v.component for v in versions]
        components = list(set(components))
        self.setColumnCount(len(components))
        self.setHorizontalHeaderLabels([f"{c.label} {c.extension}" for c in components])
        columns = {component: i for i, component in enumerate(components)}

        # rows (version numbers)
        work_versions =  components[0].stage.get_work_component().versions  # any item from components will work
        numbers: list[int] = [v.number for v in work_versions]
        numbers = list(set(numbers))
        numbers.reverse()
        self.setRowCount(len(numbers))
        self.setVerticalHeaderLabels([f"{n:03d}" for n in numbers])
        rows = {number: i for i, number in enumerate(numbers)}

        for version in versions:
            row = rows.get(version.number, None)
            column = columns.get(version.component, None)

            if row is not None and column is not None:
                text = version.creation_user.pseudo
                icon = qtawesome.icon('fa.check')
                item = QTableWidgetItem(text)
                item.setIcon(icon)
                self.setItem(row, column, item)

    def set_stage(self, stage: Stage=None):
        self.stage = stage

        if stage is None:
            return

        versions = []
        for component in stage.components:
            if component != stage.get_work_component():
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
