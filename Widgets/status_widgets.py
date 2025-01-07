from PySide6.QtWidgets import QComboBox

from Gui.palette_api import ZPalette

c = ZPalette()

class GStatusCombobox(QComboBox):
    colors = {
        "TODO": c.yellow,
        "WIP": c.orange,
        "DONE": c.green,
        "WFA": c.purple,
        "ERROR": c.red,
        "OMIT": c.light,
    }

    def __init__(self, starting_status: str = "TODO"):
        super().__init__()
        self.addItems([k for k in self.colors.keys()])
        self.view().colors = self.colors

        self.on_text_changed(self.currentText())
        self.currentTextChanged.connect(self.on_text_changed)

        if starting_status in self.colors.keys():
            self.setCurrentText(starting_status)

    def on_text_changed(self, text):
        # TODO: color the content for better ux
        pass

