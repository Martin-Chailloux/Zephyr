import qtawesome

from PySide6.QtWidgets import QTabWidget, QWidget, QMainWindow

from Gui.GuiPanels.top_menu_bar import BreezeTopMenuBar
from Gui.MainWindows.browser_main_window import BrowserGui
from Gui.MainWindows.turbine_main_window import TurbineGui


# TODO: empty tabs to switch to when not loaded
#  with stored settings for each tab


class BreezeTabs(QTabWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        self.setStyleSheet("QTabBar::tab {width: 56px;}")
        self.browser_window = BrowserGui()
        self.breeze_tab = self.addTab(self.browser_window, "Browser")

        self.turbine_window = TurbineGui()
        self.turbine_tab = self.addTab(self.turbine_window, "Turbine")

        temp_window = QMainWindow()
        temp_tab = self.addTab(temp_window, "Logs")


class BreezeMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Breeze")
        self.setWindowIcon(qtawesome.icon("fa5s.wind"))
        self._init_ui()

    def _init_ui(self):
        # top menu bar
        self.setMenuBar(BreezeTopMenuBar())

        # stage central widget
        breeze_tabs_widget = BreezeTabs()
        self.setCentralWidget(breeze_tabs_widget)

        # out vars
        self.breeze_tabs_widget = breeze_tabs_widget
