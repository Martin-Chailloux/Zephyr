"""
# ContextMenu, how tu use:
def _connect_signals(self):
    widget.customContextMenuRequested.connect(self.show_context_menu)

def show_context_menu(self, position: QPoint):
    menu = ContextMenu()
    menu.show(position=self.mapToGlobal(position))

"""

import qtawesome
from PySide6 import QtCore
from PySide6.QtCore import QPoint
from PySide6.QtGui import QAction, QMouseEvent
from qtpy.QtWidgets import QMenu


class ContextMenu(QMenu):
    def add_action(self, label: str, icon_name: str) -> QAction:
        action = self.addAction(label)
        action.setIcon(qtawesome.icon(icon_name))
        return action

    def show(self, position: QPoint):
        action = self.exec_(self.mapToGlobal(position))
        self.resolve(action)

    def resolve(self, action: QAction):
        pass

    def mousePressEvent(self, event):
        if isinstance(event, QMouseEvent):
            if event.button() == QtCore.Qt.MouseButton.RightButton:
                self.close()
        super().mousePressEvent(event)
