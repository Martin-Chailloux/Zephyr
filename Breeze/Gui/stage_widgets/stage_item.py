from textwrap import dedent

from PySide6 import QtCore
from PySide6.QtCore import QRect, Signal
from PySide6.QtGui import QPainter, QBrush, QIcon, QPainterPath, QColor
from PySide6.QtWidgets import QPushButton, QSizePolicy, QHBoxLayout, QComboBox, QWidget

import qtawesome

from Data.breeze_documents import StageTemplate, Stage
from Gui.status_widgets.status_subwidgets import SelectStatusWidget


class StageItem(QWidget):
    h = 28
    stage_selected = Signal(str)

    def __init__(self, stage: Stage):
        self.stage = stage
        super().__init__()

        self._init_ui()
        self.connect_signals()

    def __repr__(self):
        return f"StageItem|{self.stage.__repr__()}"

    def set_stage(self, stage: Stage):
        while self.layout().count():
            item = self.layout().takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.stage = stage
        self._init_ui()
        self.connect_signals()

    def _init_ui(self):
        # TODO: le layout se set pas une 2e fois si on rappelle la fonction
        #   donc on utilise self.layout() ensuite
        #   lire la doc Qt pour comprendre
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.setFixedHeight(self.h)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        # TODO: photo de profil comme icone, le nom en tooltip quand on hover
        # TODO: bigger round button with tooltip
        # TODO: offset in its own widget
        user_combobox = QComboBox()
        self.layout().addWidget(user_combobox)
        user_combobox.setFixedHeight(self.h)
        users = ["Martin", "Kim", "Elise", "Chloé", "Hugo", "Camille"]
        user_combobox.addItems(users)
        for i, user in enumerate(users):
            icon_path = f"Breeze/Resources/Icons/Users/{user.lower()}.jpg"
            icon = QIcon(icon_path)
            user_combobox.setItemIcon(i, icon)
            user_combobox.setToolTip("UserTest")

        button = StageButton(template=self.stage.stage_template, h=self.h)
        self.layout().addWidget(button)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        status_button = SelectStatusWidget(height=self.h)
        self.layout().addWidget(status_button)

        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # public vars
        self.button = button

    def connect_signals(self):
        self.button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        if self.button.isChecked():
            self.stage_selected.emit(self.stage.longname)


class StageButton(QPushButton):
    unchecked_alpha: float = 0.3

    def __init__(self, template: StageTemplate, h: int=28):
        super().__init__()
        self.template = template
        self.h = h
        self._init_ui()

    def _init_ui(self):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCheckable(True)
        self.setStyleSheet(dedent("""
            QPushButton {
                color: darkgrey;
                text-align: left;
                padding-left: 48 px;
            }
            QPushButton:checked {
                color: white;
                border: 1px solid white;
                text-align: left;
                padding-left: 48 px;
            }
        """))
        self.setFixedHeight(self.h)
        self.setText(self.template.label)

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color = QColor(self.template.color)
        if not self.isChecked():
            color.setAlphaF(self.unchecked_alpha)
        painter.setBrush(QBrush(color))
        painter.setPen("white")

        rect: QRect = event.rect()
        x = rect.x()
        y = rect.y()
        w = rect.width()
        h = rect.height()

        # Fill color
        fill_w = 36
        rect.setWidth(fill_w)
        border_width = 1
        rect = QRect(x + border_width, y + border_width, fill_w + border_width, h - border_width*2)
        path = QPainterPath()
        path.addRoundedRect(rect, 3, 3)
        painter.fillPath(path, painter.brush())

        # Icon
        margin = 2
        rect.setX(x)
        rect.setY(y+margin)
        rect.setWidth(fill_w)
        rect.setHeight(h - margin*2)

        opacity = 1 if self.isChecked() else self.unchecked_alpha
        icon: QIcon = qtawesome.icon(self.template.icon_name, opacity=opacity)
        icon.paint(painter, rect, QtCore.Qt.AlignmentFlag.AlignRight)

        painter.restore()
