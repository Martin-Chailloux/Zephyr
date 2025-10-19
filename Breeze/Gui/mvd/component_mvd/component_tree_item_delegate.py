from typing import Optional

import qtawesome
from PySide6 import QtCore
from PySide6.QtCore import QModelIndex, QRect, QTimer
from PySide6.QtGui import QPainter, QStandardItemModel
from PySide6.QtWidgets import QStyleOptionViewItem, QComboBox, QStyle, QWidget

from Api.document_models.project_documents import Component, Version, Stage
from Api.recipes.ingredients import IngredientSlot
from Gui.mvd.abstract_mvd import AbstractItemDelegate
from Gui.mvd.component_mvd.component_tree_model import ComponentTreeItemRoles, ComponentTreeModel
from Gui.popups.component_browser import ComponentBrowser

alignment = QtCore.Qt.AlignmentFlag


# TODO:
#   - search with filters
#   - add extra slot only if it does not exist yet (hard refresh should solve this)
#   - version pill
#   - is_multiple pill
#   - delete ingredients
#   - select version


class ComponentTreeItemDelegate(AbstractItemDelegate):
    is_tree = True

    def __init__(self):
        super().__init__()
        self.stage: Optional[Stage] = None

    def _set_custom_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        self.is_title: bool = index.data(ComponentTreeItemRoles.is_title)

        if self.is_title:
            self.label: str = index.data(ComponentTreeItemRoles.label)
        else:
            self.version: Version = index.data(ComponentTreeItemRoles.version)

    def set_stage(self, stage: Optional[Stage]):
        self.stage = stage

    def paint(self, painter: QPainter, option: QStyleOptionViewItem , index: QModelIndex):
        self._set_data(option, index)
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
            self.paint_component(painter, component=self.version.component)

        painter.restore()

    def paint_title(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()

        painter.save()
        text = f" {self.label}"
        rect = QRect(x, y, w, h)
        painter.drawText(rect, text, alignment.AlignLeft | alignment.AlignVCenter)
        painter.restore()

    def paint_create(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        margin = 4 if self.is_hovered or self.is_selected else 5

        painter.save()

        icon = qtawesome.icon('fa.plus-circle')
        rect = QRect(x, y+margin, h, h-2*margin)
        icon.paint(painter, rect, QtCore.Qt.AlignmentFlag.AlignCenter)
        painter.restore()

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        if index.data(ComponentTreeItemRoles.is_title):
            super().createEditor(parent, option, index)
            return

        components = Component.objects
        browser = ComponentBrowser(components=components)
        browser.setWindowFlags(QtCore.Qt.WindowType.Tool)
        QTimer.singleShot(0, lambda: browser.move(parent.mapToGlobal(option.rect.topLeft())))
        QTimer.singleShot(0, lambda: browser.setMinimumSize(0, 0))
        QTimer.singleShot(0, lambda: browser.setMaximumSize(500, 500))
        QTimer.singleShot(0, lambda: browser.resize(280, 280))
        browser.setFocus()
        return browser

    def setModelData(self, editor: ComponentBrowser, model: ComponentTreeModel, index: QModelIndex):
        component = editor.component_list.get_selected_component()
        if component is None:
            return

        new_version = component.get_last_version()
        if new_version is None:
            return

        # update the stage
        ingredient_slot: IngredientSlot = index.data(ComponentTreeItemRoles.ingredient_slot)
        current_version: Version = index.data(ComponentTreeItemRoles.version)
        if current_version is None:
            self.stage.add_ingredient(name=ingredient_slot.name, version=new_version)
        else:
            self.stage.replace_ingredient(name=ingredient_slot.name,
                                          old_version=current_version,
                                          new_version=new_version)

        # update the model
        model.setData(index, new_version, ComponentTreeItemRoles.version)
        model.itemFromIndex(index).setSelectable(True)  # the item now has a version, so it should be selectable

        if ingredient_slot.is_multiple:
            # add an empty item to add more ingredients
            model.add_sub_item(parent=model.itemFromIndex(index.parent()), ingredient_slot=ingredient_slot, version=None)


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
