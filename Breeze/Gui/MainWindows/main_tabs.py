import qtawesome

from PySide6.QtWidgets import QTabWidget, QWidget, QMainWindow

from Gui.GuiPanels.top_menu_bar import BreezeTopMenuBar
from Gui.MainWindows.breeze_main_window import BreezeWindow


# TODO: empty tabs to switch to when not loaded
#  with stored settings for each tab


class BreezeTabs(QTabWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        self.breeze_window = BreezeWindow()
        self.breeze_tab = self.addTab(self.breeze_window, "Breeze")

        self.turbine_window = TurbineGui()
        self.turbine_tab = self.addTab(self.turbine_window, "Turbine")


class TurbineGui(QWidget):
    def __init__(self):
        super().__init__()


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
