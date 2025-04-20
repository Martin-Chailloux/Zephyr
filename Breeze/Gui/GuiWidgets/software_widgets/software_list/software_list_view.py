from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtGui import QMouseEvent

from Data.project_documents import Stage
from Gui.GuiWidgets.abstract_widgets.abstract_mvd import AbstractListView
from Gui.GuiWidgets.software_widgets.software_list.software_list_item_delegate import SoftwareListItemDelegate
from Gui.GuiWidgets.software_widgets.software_list.software_list_model import SoftwareListModel, SoftwareItemRoles


class SoftwareListView(AbstractListView):
    software_selected = Signal(str)
    right_clicked = Signal()

    def __init__(self, stage: Stage):
        super().__init__()
        self._model = SoftwareListModel(stage=stage)
        self.setModel(self._model)

        self._item_delegate = SoftwareListItemDelegate()
        self.setItemDelegate(self._item_delegate)

    def mousePressEvent(self, event):
        if isinstance(event, QMouseEvent):
            if event.button() == QtCore.Qt.MouseButton.RightButton:
                self.right_clicked.emit()
                return

        super().mousePressEvent(event)
        hovered_item = self._get_hovered_item()
        if hovered_item is None:
            return
        software = hovered_item.data(SoftwareItemRoles.software)
        self.software_selected.emit(software.label)
