import qtawesome

from PySide6.QtWidgets import QTabWidget, QMainWindow

from Api.breeze_app import BreezeApp
from Gui.main_windows.top_menu_bar import BreezeTopMenuBar
from Gui.main_windows.browser import BrowserGui
from Gui.main_windows.turbine import TurbineGui


# TODO: empty tabs to switch to when not loaded
#  with stored settings for each tab


class BreezeTabs(QTabWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        self.setStyleSheet("QTabBar::tab {width: 56px;}")
        self.browser_window = BrowserGui()
        self.browser_tab = self.addTab(self.browser_window, "Browser")

        self.turbine_window = TurbineGui()
        self.turbine_tab = self.addTab(self.turbine_window, "Turbine")

        admin_window = QMainWindow()  # replace when it exists
        admin_tab = self.addTab(admin_window, "Admin")

        self.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self):
        match self.currentIndex():
            case 1:  # turbine
                self.turbine_window.refresh()
            case _:
                pass


class BreezeMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Breeze")
        self.setWindowIcon(qtawesome.icon("fa5s.wind"))
        self._init_ui()

    def _init_ui(self):
        # top menu bar
        # self.setMenuBar(BreezeTopMenuBar())
        top_menu_bar = BreezeTopMenuBar()
        self.setMenuWidget(top_menu_bar)

        # stage central widget
        tabs = BreezeTabs()
        self.setCentralWidget(tabs)

        # out vars
        self.top_menu_bar = top_menu_bar
        self.tabs = tabs

        self.top_menu_bar.project_changed.connect(self.on_project_changed)

    def on_project_changed(self):
        print(f"PROJECT CHANGED: {BreezeApp.project = }")
        self.tabs.browser_window.refresh()
        self.tabs.turbine_window.refresh()