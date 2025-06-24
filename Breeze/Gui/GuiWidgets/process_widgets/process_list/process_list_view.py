import importlib

from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtGui import QMouseEvent

from Data.project_documents import StageTemplate
from Data.studio_documents import Process
from Gui.GuiWidgets.abstract_widgets.abstract_mvd import AbstractListView
from Gui.GuiWidgets.process_widgets.process_list.process_list_item_delegate import ProcessListItemDelegate
from Gui.GuiWidgets.process_widgets.process_list.process_list_model import ProcessListModel, ProcessItemRoles
from Turbine.tb_core import ProcessStep


class ProcessListView(AbstractListView):
    process_selected = Signal(str)
    right_clicked = Signal()

    def __init__(self):
        super().__init__()
        self._model = ProcessListModel()
        self.setModel(self._model)

        self._item_delegate = ProcessListItemDelegate()
        self.setItemDelegate(self._item_delegate)

        self.selectionModel().selectionChanged.connect(self.on_selection_changed)

    def mousePressEvent(self, event):
        if isinstance(event, QMouseEvent):
            if event.button() == QtCore.Qt.MouseButton.RightButton:
                self.right_clicked.emit()
                return

        super().mousePressEvent(event)
    #     hovered_item = self.get_hovered_item()
    #     if hovered_item is None:
    #         return
    #     process: MgProcess = hovered_item.data(ProcessItemRoles.process)
    #     self.process_selected.emit(process.longname)

    def set_stage_template(self, stage_template: StageTemplate):
        self._model.populate(processes=stage_template.processes)

    def get_selected_process(self) -> ProcessStep.__class__ | None:
        items = self.get_selected_items()
        if not items:
            return None
        else:
            process: Process = items[0].data(ProcessItemRoles.process)
            path = process.class_path
            module_name, class_name = path.rsplit('.', 1)
            module = importlib.import_module(module_name)
            process: ProcessStep.__class__ = getattr(module, class_name)
            return process

    def on_selection_changed(self):
        process = self.get_selected_process()
        print(f"{process = }")
        self.process_selected.emit(process)
