from PySide6.QtWidgets import QComboBox

from Gui.palette_api import ZPalette

c = ZPalette()

class ZStatusComboBox(QComboBox):
    colors = {
        "WAIT": c.yellow,
        "TODO": c.yellow,
        "WIP": c.orange,
        "DONE": c.green,
        "WFA": c.purple,
        "ERROR": c.red,
        "OMIT": c.light,
    }

    def __init__(self, starting_status: str = "TODO"):
        # TODO: les choix doivent venir de lq db
        super().__init__()
        self.addItems([k for k in self.colors.keys()])
        self.view().colors = self.colors

        self.on_text_changed(self.currentText())
        self.currentTextChanged.connect(self.on_text_changed)

        if starting_status in self.colors.keys():
            self.setCurrentText(starting_status)

    def on_text_changed(self, text):
        # TODO: colorize the content for better ux
        pass

