import qtawesome
from PySide6 import QtCore
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout

from Data.project_documents import Stage
from Data.studio_documents import Software
from Gui.GuiWidgets.abstract_widgets.context_menu_widget import ContextMenuWidget
from Gui.GuiWidgets.software_widgets.software_list.software_list_view import SoftwareListView
from Gui.GuiWidgets.util_widgets.util_widgets import TextBox, IconButton


class SoftwareSelectMenu(ContextMenuWidget):
    def __init__(self, stage: Stage):
        super().__init__(w=168, h=248, position=[0.5, 0.25])
        self.stage = stage
        self.software: Software = None  # is set when closed
        self.comment: str = None  # is set when closed
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        software_list = SoftwareListView(stage=self.stage)
        layout.addWidget(software_list)
        # software_list.set_selected_user(self.stage.user)

        self.software_list = software_list

    def _connect_signals(self):
        self.software_list.software_selected.connect(self.on_software_selected)
        self.software_list.right_clicked.connect(self.close)


    def on_software_selected(self, label: str):
        comment_box = CommentEditMenu(title="Comment: ", default_comment="New file")
        comment_box.exec()

        software = Software.objects.get(label=label)
        self.software = software
        self.comment = comment_box.comment

        self.is_canceled = comment_box.is_canceled
        self.close()


class CommentEditMenu(ContextMenuWidget):
    def __init__(self, title: str=None, default_comment: str=None):
        super().__init__(w=168, h=168, position=[0.5, 0.3], show_borders=False)
        self.title = title
        self.default_comment: str = default_comment

        self._init_ui()
        self._connect_signals()
        self._connect_shortcuts()
        self._set_initial_state()

        self.setShortcutEnabled(True)
        # It is canceled by default and does nothing on close
        # When confirmed, it switches to not canceled
        self.is_canceled = True

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)

        textbox = TextBox(title=self.title)
        layout.addWidget(textbox)
        textbox.text_edit.setText(self.default_comment)

        sub_layout = QHBoxLayout()
        layout.addLayout(sub_layout)
        confirm_button = QPushButton("Confirm")
        sub_layout.addWidget(confirm_button)
        confirm_button.setIcon(qtawesome.icon("fa.check"))
        confirm_button.setFixedHeight(24)

        cancel_button = IconButton(icon_name="fa.close",  width=24)
        sub_layout.addWidget(cancel_button)

        self.textbox = textbox
        self.confirm_button = confirm_button
        self.cancel_button = cancel_button

    @property
    def comment(self) -> str:
        text = self.textbox.text_edit.toPlainText()
        return text

    def _connect_signals(self):
        self.textbox.text_edit.textChanged.connect(self.on_text_changed)
        self.confirm_button.clicked.connect(self.on_confirm)
        self.cancel_button.clicked.connect(self.close)

    def _connect_shortcuts(self):
        modifiers = QtCore.Qt.Modifier
        keys = QtCore.Qt.Key

        confirm = QShortcut(QKeySequence(modifiers.CTRL | keys.Key_Return), self)
        confirm.activated.connect(self.on_confirm)

    def _set_initial_state(self):
        self.on_text_changed()
        self.textbox.text_edit.selectAll()

    def on_text_changed(self):
        # TODO: create class BreezeComment in breeze_converters.py to manage the comments
        is_valid: bool = 3 < len(self.comment) < 100
        self.confirm_button.setEnabled(is_valid)

    def on_confirm(self):
        print(f"CONFIRM")
        if not self.confirm_button.isEnabled():
            return
        self.is_canceled = False
        self.close()