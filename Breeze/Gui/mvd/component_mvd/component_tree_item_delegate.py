from typing import Optional

import qtawesome
from PySide6 import QtCore
from PySide6.QtCore import QModelIndex, QRect
from PySide6.QtGui import QPainter, QCursor
from PySide6.QtWidgets import QStyleOptionViewItem,  QWidget

from Api.document_models.project_documents import Version, Stage
from Api.recipes.ingredient_slot import IngredientSlot
from Gui.mvd.abstract_mvd import AbstractItemDelegate
from Gui.mvd.component_mvd.component_tree_model import (ComponentTreeItemRoles, ComponentTreeModel,
                                                        ComponentTreeItemMetrics)
from Gui.popups.component_browser import ComponentBrowser
from Gui.popups.version_browser import VersionBrowser

alignment = QtCore.Qt.AlignmentFlag


# TODO:
#   - search with filters


class ComponentTreeItemDelegate(AbstractItemDelegate):
    is_tree = True

    def __init__(self):
        super().__init__()
        self.stage: Optional[Stage] = None

    def _set_custom_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        self.is_title: bool = index.data(ComponentTreeItemRoles.is_title)
        self.can_edit_version_number: bool = index.data(ComponentTreeItemRoles.can_edit_version_number)
        # self.ingredient_slot  # avoid: not consistent with popups

        if self.is_title:
            self.label: str = index.data(ComponentTreeItemRoles.label)
        else:
            self.version: Version = index.data(ComponentTreeItemRoles.version)

    def set_stage(self, stage: Optional[Stage]):
        self.stage = stage

    def paint(self, painter: QPainter, option: QStyleOptionViewItem , index: QModelIndex):
        self._set_data(option, index)
        x, y, w, h = self.get_item_rect()
        ingredient_slot: IngredientSlot = index.data(ComponentTreeItemRoles.ingredient_slot)

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.paint_selected_background(painter)
        self.paint_hover(painter)
        self.paint_selected_underline(painter)

        if self.is_title:
            self.paint_title(painter, is_multiple=ingredient_slot.is_multiple)
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

    def paint_title(self, painter: QPainter, is_multiple: bool):
        x, y, w, h = self.get_item_rect()

        painter.save()

        # paint text
        text = f" {self.label}"
        if not is_multiple:
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
    def create_component_editor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        # filter allowed components
        ingredient_slot: IngredientSlot = index.data(ComponentTreeItemRoles.ingredient_slot)
        components = ingredient_slot.allowed_components

        # create editor
        components_browser = ComponentBrowser(components=components, stage=self.stage)
        return components_browser

    def create_version_number_editor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        # get work versions with same number as available component's versions
        version: Version = index.data(ComponentTreeItemRoles.version)
        work_component = version.component.stage.work_component
        available_versions = version.component.versions
        available_versions_numbers = [v.number for v in available_versions]
        versions = [v for v in work_component.versions if v.number in available_versions_numbers]

        # create editor
        version_browser = VersionBrowser(versions=versions)
        return version_browser

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        is_title = index.data(ComponentTreeItemRoles.is_title)
        if is_title:
            super().createEditor(parent, option, index)
            return

        can_edit_version_number = index.data(ComponentTreeItemRoles.can_edit_version_number)
        if can_edit_version_number:
            editor = self.create_version_number_editor(parent=parent, option=option, index=index)
        else:
            editor = self.create_component_editor(parent=parent, option=option, index=index)
        editor.setWindowFlags(QtCore.Qt.WindowType.Popup)
        self.is_editing = False
        return editor

    def updateEditorGeometry(self, editor, option, index):
        if self.is_editing:
            return

        editor.move(QCursor.pos())
        self.is_editing = True

    def set_version_number_data(self, editor: VersionBrowser, model: ComponentTreeModel, index: QModelIndex):
        selected_version = editor.versions_list.get_selected_version()
        if selected_version is None:
            return

        # get new version
        current_version: Version = index.data(ComponentTreeItemRoles.version)
        new_version = current_version.component.get_version(number=selected_version.number)

        ingredient_slot: IngredientSlot = index.data(ComponentTreeItemRoles.ingredient_slot)
        self.stage.replace_ingredient(name=ingredient_slot.name,
                                      old_version=current_version,
                                      new_version=new_version)

    def set_component_data(self, editor: ComponentBrowser, model: ComponentTreeModel, index: QModelIndex):
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


    def setModelData(self, editor: VersionBrowser | ComponentBrowser, model: ComponentTreeModel, index: QModelIndex):
        is_title = index.data(ComponentTreeItemRoles.is_title)
        if is_title:
            super().setModelData(editor, model, index)
            return

        accepted: bool = bool(editor.result())
        if not accepted:
            return

        can_edit_version_number = index.data(ComponentTreeItemRoles.can_edit_version_number)
        if can_edit_version_number:
            self.set_version_number_data(editor=editor, model=model, index=index)
        else:
            self.set_component_data(editor=editor, model=model, index=index)

        # refresh
        model.refresh_view.emit()
