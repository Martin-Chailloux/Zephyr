import qtawesome
from PySide6 import QtCore
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMenuBar, QMenu


modifiers = QtCore.Qt.Modifier
keys = QtCore.Qt.Key


class TopMenuBar(QMenuBar):
    def __init__(self):
        super().__init__()
        # settings_menu = self.add_menu(self, label="Settings", icon_name="fa.gear")  # Not needed yet
        palette_menu = self.add_menu(self,  label="Palette",  icon_name="fa.paint-brush")
        project_menu = self.add_menu(self,  label="Project",  icon_name="fa.tv")
        user_menu = self.add_menu(self,     label="User",     icon_name="fa5s.user-circle")

        self.add_action(palette_menu, label="Breeze")
        self.add_action(palette_menu, label="Dark")
        self.add_action(palette_menu, label="Light")

        self.add_action(project_menu, label="Switch")
        self.add_action(project_menu, label="Edit", shortcut=keys.Key_E)

        self.add_action(user_menu, label="Switch", shortcut=keys.Key_S)
        self.add_action(user_menu, label="Edit", shortcut=keys.Key_E)


    def add_menu(self, parent: QMenuBar | QMenu, label: str, icon_name: str) -> QMenu:
        # TODO: tooltips are not working
        #  not needed for now
        menu = QMenu(label, self)
        parent.addMenu(menu)
        menu.setIcon(qtawesome.icon(icon_name))
        menu.setStyleSheet("QMenu::item {padding: 4px 12px 4px 12px;}")
        return menu

    def add_action(self, parent: QMenu, label: str, icon_name: str=None, shortcut: QtCore.Qt.Key|QKeySequence=None) -> QAction:
        action = QAction(label, self)
        parent.addAction(action)
        if icon_name is not None:
            action.setIcon(qtawesome.icon(icon_name))
        # if shortcut is not None:
        #     action.setShortcut(shortcut)
        # action.setShortcutVisibleInContextMenu(False)
        return action
