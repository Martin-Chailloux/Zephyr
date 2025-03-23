import qtawesome

from Dialogs.palette_dialog import Palette
from Gui.util_widgets.util_widgets import IconButton


class SetBookmarkIconButton(IconButton):
    palette: Palette = Palette.objects.get(name="dev")

    def __init__(self):
        super().__init__(icon_name="fa.star", width=24, icon_size=18, color=self.palette.white_text)
        self.unchecked_icon = qtawesome.icon("fa.star-o", color=self.color)

        self.setCheckable(True)
        self.clicked.connect(self.on_click)

        self.set_state(is_checked=False)  # TODO: from db

    def on_click(self, is_checked: bool):
        icon = self.icon if is_checked else self.unchecked_icon
        self.setIcon(icon)

    def set_state(self, is_checked: bool):
        self.setChecked(is_checked)
        self.on_click(is_checked=is_checked)
