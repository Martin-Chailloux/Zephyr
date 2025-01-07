from PySide6.QtGui import QCursor

from PySide6 import QtCore
from PySide6.QtWidgets import (QVBoxLayout, QTableWidget, QLineEdit, QHBoxLayout,
                               QPushButton, QTableWidgetItem, QMessageBox, QMenu)
import qtawesome

from MangoEngine import mongo_dialog
from Widgets.qt_extensions import ZIconButton


class ZFakeIngestWidget(QTableWidget):
    def __init__(self,):
        super().__init__()
        self._init_ui()
        self.connect_signals()
        self.table.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.setContentsMargins(0, 0, 0, 0)

        table = GIngestTable()
        layout.addWidget(table)

        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)
        h_layout.setSpacing(2)

        copy_button = ZIconButton("fa5s.clone", 30, 20)
        h_layout.addWidget(copy_button)

        plus_button = ZIconButton("fa.plus", 30, 20)
        h_layout.addWidget(plus_button)

        minus_button = ZIconButton("fa.minus", 30, 20)
        h_layout.addWidget(minus_button)

        h_layout.addSpacing(7)

        name_field = QLineEdit()
        h_layout.addWidget(name_field)

        rename_button = ZIconButton("mdi6.rename", 30, 20)
        h_layout.addWidget(rename_button)

        export_button = QPushButton("Save to Database")
        export_button.setIcon(qtawesome.icon("fa.save"))
        export_button.setMinimumHeight(33)
        layout.addWidget(export_button)

        # --- public vars ---

        self.table = table

        self.copy_button = copy_button
        self.plus_button = plus_button
        self.minus_button = minus_button
        self.name_field = name_field
        self.rename_button = rename_button
        self.save_button = export_button

    def connect_signals(self):
        self.copy_button.clicked.connect(self.table.copy_row)
        self.plus_button.clicked.connect(self.table.add_row)
        self.minus_button.clicked.connect(self.table.delete_rows)
        self.rename_button.clicked.connect(self.on_rename_button_clicked)
        self.save_button.clicked.connect(self.on_save_button_clicked)

    def on_rename_button_clicked(self):
        text = self.name_field.text()
        self.table.rename_selection(text)

    def on_save_button_clicked(self):
        popup = QMessageBox()
        popup.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg = "\n".join(self.table.long_names)
        popup.setText(msg)
        confirm = popup.exec()
        yes = confirm == 16384
        if yes:
            for name in self.table.long_names:
                stage = mongo_dialog.Stage.from_long_name(name)
                stage.save()


class GIngestTable(QTableWidget):
    presets: dict[list[str]] = {
        "category": ["character", "props", "element", "decor"],
        "name": [],
        "variant": [],
        "description": ["modeling", "texturing", "shading", "rigging"],
        "detail": ["assembly"],
        "extension": [".blend", ".ma", ".hou", ".spp"],
    }

    def __init__(self,):
        super().__init__(0, 6)
        self._init_ui()

    def _init_ui(self):
        self.setHorizontalHeaderLabels(["category", "name", "variant", "description", "detail", "extension"])
        self.add_row()

    @property
    def selected_rows(self):
        return [item.row() for item in self.selectedIndexes()]

    @property
    def long_names(self) -> list[str]:
        long_names = []
        for row in range(self.rowCount()):
            long_name = []
            for column in range(self.columnCount()):
                item = self.item(row, column)
                text = "-" if item is None else "-" if item.text() == "" else item.text()
                long_name.append(text)
            long_names.append("_".join(long_name))
        return long_names

    def copy_row(self):
        for row in list(dict.fromkeys(self.selected_rows)):
            items = [self.item(row, column) for column in range(self.columnCount())]
            self.add_row()
            for column in range(self.columnCount()):
                if items[column] is not None:
                    item = QTableWidgetItem(items[column].text())
                    self.setItem(self.rowCount()-1, column, item)

    def add_row(self):
        self.setRowCount(self.rowCount() + 1)

    def delete_rows(self):
        while self.selected_rows:
            self.removeRow(self.selected_rows[0])

    def rename_selection(self, text: str):
        for item in self.selectedIndexes():
            self.setItem(item.row(), item.column(), QTableWidgetItem(text))

    def mousePressEvent(self, event):
        old_item = self.indexAt(event.pos())
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            menu = QMenu()
            for i, preset in enumerate(self.presets.keys()):
                if old_item.column() == i:
                    for action in self.presets[preset]:
                        menu.addAction(action)

            choice = menu.exec(QCursor.pos())
            if choice is None:
                return
            else:
                new_item = QTableWidgetItem(choice.text())
                self.setItem(old_item.row(), old_item.column(), new_item)

        if event.button() == QtCore.Qt.MouseButton.MiddleButton:
            new_item = QTableWidgetItem("")
            self.setItem(old_item.row(), old_item.column(), new_item)

        super().mousePressEvent(event)

