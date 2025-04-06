from textwrap import dedent

from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGridLayout, QPushButton

from Data.studio_documents import Status, Palette
from Data.project_documents import Stage
from Gui.abstract_widgets.context_menu_widget import ContextMenuWidget


def create_status(label: str, color: str, order: int) -> Status:
    status = Status(label=label, color=color, order=order)
    status.save()
    return status


class EditStatusMenu(ContextMenuWidget):
    palette: Palette = Palette.objects.get(name="dev")
    statuses = Status.objects
    statuses = sorted(statuses, key=lambda x: x.order)
    margin = 2
    spacing = 1
    button_w = 48
    button_h = 28
    max_columns = 2

    def __init__(self, stage: Stage):
        self.stage = stage
        self.status_per_label: dict[str, Status] = {}

        max_rows = int(len(self.statuses) / self.max_columns) + 1
        w = (self.button_w * self.max_columns) + (2 * self.margin)
        h = (self.button_h * max_rows) + (2 * self.margin)

        super().__init__(w=w, h=h,
                         align_h=QtCore.Qt.AlignmentFlag.AlignHCenter,
                         align_v=QtCore.Qt.AlignmentFlag.AlignVCenter)
        self._init_ui()

    def _init_ui(self):
        layout = QGridLayout()
        self.setLayout(layout)
        layout.setContentsMargins(self.margin, self.margin, self.margin, self.margin)
        layout.setSpacing(self.spacing)

        for i, status in enumerate(self.statuses):
            button = QPushButton(status.label)
            set_stylesheet(button, status.color)
            button.clicked.connect(self.on_button_clicked)
            button.setFixedSize(QSize(self.button_w, self.button_h))
            self.status_per_label[button.text()] = status

            row = int(i / self.max_columns)
            column = i % self.max_columns
            layout.addWidget(button, row, column)

    def on_button_clicked(self):
        # TODO: subclass button to send more infos than label
        button: QPushButton = self.sender()
        status = self.status_per_label[button.text()]
        print(f"Selected status: {status}")

        self.stage.set_status(status=status)

        self.close()


def set_stylesheet(widget, color: str):
    hover_color = QColor(color).lighter(110).name()
    widget.setStyleSheet(dedent("""
                    QPushButton {
                        color: black ;
                        background-color: $color;
                        border: 2px solid transparent;
                    }
                    QPushButton:hover {
                        background-color: $hover_color;
                        border: none;
                    }
                    """)
                    .replace("$color", color)
                    .replace("$hover_color", hover_color))
