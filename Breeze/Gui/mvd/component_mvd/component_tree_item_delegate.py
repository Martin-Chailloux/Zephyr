from typing import Optional

import qtawesome
from PySide6 import QtCore
from PySide6.QtCore import QModelIndex, QRect, QTimer
from PySide6.QtGui import QPainter, QStandardItemModel
from PySide6.QtWidgets import QStyleOptionViewItem, QComboBox, QStyle, QWidget

from Api.document_models.project_documents import Component, Version, Stage
from Api.recipes.ingredient_slot import IngredientSlot
from Gui.mvd.abstract_mvd import AbstractItemDelegate
from Gui.mvd.component_mvd.component_tree_model import ComponentTreeItemRoles, ComponentTreeModel, \
    ComponentTreeItemMetrics
from Gui.popups.component_browser import ComponentBrowser

alignment = QtCore.Qt.AlignmentFlag


# TODO:
#   - search with filters
#   - select version


class ComponentTreeItemDelegate(AbstractItemDelegate):
    is_tree = True

    def __init__(self):
        super().__init__()
        self.stage: Optional[Stage] = None

    def _set_custom_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        self.is_title: bool = index.data(ComponentTreeItemRoles.is_title)
        self.ingredient_slot: IngredientSlot = index.data(ComponentTreeItemRoles.ingredient_slot)
        self.can_edit_version_number: bool = index.data(ComponentTreeItemRoles.can_edit_version_number)

        if self.is_title:
            self.label: str = index.data(ComponentTreeItemRoles.label)
        else:
            self.version: Version = index.data(ComponentTreeItemRoles.version)

    def set_stage(self, stage: Optional[Stage]):
        self.stage = stage

    def paint(self, painter: QPainter, option: QStyleOptionViewItem , index: QModelIndex):
        self._set_data(option, index)
        x, y, w, h = self.get_item_rect()

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.paint_selected_background(painter)
        self.paint_hover(painter)
        self.paint_selected_underline(painter)

        if self.is_title:
            self.paint_title(painter)
        elif self.version is None:
            self.paint_create(painter)
        else:
            version_width = ComponentTreeItemMetrics.version_width
            edit_width = ComponentTreeItemMetrics.edit_width
            component_width = w-version_width
            if self.is_hovered and self.can_edit_version_number:
                component_width -= edit_width / 2

            self.paint_component(painter, component=self.version.component, width=component_width)
            if self.is_hovered and self.can_edit_version_number:
                self.paint_edit_version(painter, width=edit_width)
            self.paint_version_number(painter, number=self.version.number, x_offset=component_width, width=version_width, opacity=1)

        painter.restore()

    def paint_title(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()

        painter.save()

        # paint text
        text = f" {self.label}"
        if not self.ingredient_slot.is_multiple:
            text += " (1)"
        rect = QRect(x, y, w, h)
        painter.drawText(rect, text, alignment.AlignLeft | alignment.AlignVCenter)

        painter.restore()

    def paint_create(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        margin = 4 if self.is_hovered or self.is_selected else 5

        painter.save()
        icon = qtawesome.icon('fa.plus-circle')
        rect = QRect(x, y+margin, h, h-2*margin)
        icon.paint(painter, rect, alignment.AlignCenter)
        painter.restore()

    def paint_edit_version(self, painter: QPainter, width: int):
        x, y, w, h = self.get_item_rect()
        margin = 6

        painter.save()

        icon = qtawesome.icon('fa5s.edit')
        rect = QRect(x+w-width, y+margin, width, h-2*margin)
        icon.paint(painter, rect)

        painter.restore()

    # ------------------------
    # Editor
    # ------------------------

    def create_component_editor(self, parent: QWidget, option: QStyleOptionViewItem):
        components = Component.objects
        browser = ComponentBrowser(components=components)
        browser.setWindowFlags(QtCore.Qt.WindowType.Tool)
        QTimer.singleShot(0, lambda: browser.move(parent.mapToGlobal(option.rect.topLeft())))
        QTimer.singleShot(0, lambda: browser.setMinimumSize(0, 0))
        QTimer.singleShot(0, lambda: browser.setMaximumSize(500, 500))
        QTimer.singleShot(0, lambda: browser.resize(280, 280))
        browser.setFocus()
        return browser


    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        is_title = index.data(ComponentTreeItemRoles.is_title)
        if is_title:
            super().createEditor(parent, option, index)
            return

        can_edit_version_number = index.data(ComponentTreeItemRoles.can_edit_version_number)
        if can_edit_version_number:
            print(f"EDIT VERSION")
            editor = None
        else:
            editor = self.create_component_editor(parent=parent, option=option)
        return editor

    def set_component_data(self, editor: ComponentBrowser, model: ComponentTreeModel, index: QModelIndex):
        component = editor.component_list.get_selected_component()
        if component is None:
            return

        new_version = component.get_last_version()
        if new_version is None:
            return

        # update the stage
        # note: can't use self.ingredient_slot because it changes while the popup is opened
        ingredient_slot = index.data(ComponentTreeItemRoles.ingredient_slot)
        current_version: Version = index.data(ComponentTreeItemRoles.version)
        if current_version is None:
            self.stage.add_ingredient(name=ingredient_slot.name, version=new_version)
        else:
            self.stage.replace_ingredient(name=ingredient_slot.name,
                                          old_version=current_version,
                                          new_version=new_version)

    def setModelData(self, editor: ComponentBrowser, model: ComponentTreeModel, index: QModelIndex):
        is_title = index.data(ComponentTreeItemRoles.is_title)
        if is_title:
            super().setModelData(editor, model, index)
            return

        can_edit_version_number = index.data(ComponentTreeItemRoles.can_edit_version_number)
        if can_edit_version_number:
            print(f"EDIT VERSION")
        else:
            self.set_component_data(editor=editor, model=model, index=index)

        # refresh
        model.refresh()


class ComponentVersionTreeItemDelegate(AbstractItemDelegate):
    def paint(self, painter: QPainter, option: QStyleOptionViewItem , index: QModelIndex):
        if index.data(ComponentTreeItemRoles.is_combobox):
            self.paint_combobox(painter, option, index)

    def _create_combobox(self, parent: QWidget):
        combobox = QComboBox(parent)
        combobox.addItems(['003', '002', '001'])  # TODO: cast items from model's infos, = show current text data
        return combobox

    def paint_combobox(self, painter: QPainter, option: QStyleOptionViewItem , index: QModelIndex):
        painter.save()
        combobox = self._create_combobox(parent=None)
        if option.state & QStyle.State_MouseOver:
            pass
            # TODO: add this to the stylesheet
            #  combobox.setProperty("hovered", True)  # Simulate hover
        combobox.resize(option.rect.size())
        pixmap = combobox.grab()
        painter.drawPixmap(option.rect.topLeft(), pixmap)
        painter.restore()

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        if not index.data(ComponentTreeItemRoles.is_combobox):
            return
        combobox = self._create_combobox(parent)
        QTimer.singleShot(0, combobox.showPopup)
        return combobox

    def setEditorData(self, editor: QComboBox, index: QModelIndex):
        value = index.data()
        i = editor.findText(value)
        if i >= 0:
            editor.setCurrentIndex(i)

    def setModelData(self, editor:QComboBox, model: QStandardItemModel, index: QModelIndex):
        model.setData(index, editor.currentText())
