import qtawesome

from Api.breeze_app import BreezeApp
from Utils.sub_widgets import IconButton


class BookmarkIconButton(IconButton):
    def __init__(self):
        super().__init__(icon_name="fa.star", wh=24, icon_size=18, color=BreezeApp.palette.white_text)
        self.unchecked_icon = qtawesome.icon("fa.star-o", color=self.color)

        self.setCheckable(True)
        self.setChecked(False)
        self.clicked.connect(self.set_state)

    def setChecked(self, is_checked: bool):
        super().setChecked(is_checked)
        icon = self.icon if is_checked else self.unchecked_icon
        self.setIcon(icon)

    def set_state(self, is_checked: bool):
        self.setChecked(is_checked)
