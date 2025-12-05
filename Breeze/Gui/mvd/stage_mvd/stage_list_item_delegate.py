from PySide6 import QtCore
from PySide6.QtCore import QModelIndex, QRect, QPoint
from PySide6.QtGui import QPainter, QBrush, QPainterPath, QCursor
from PySide6.QtWidgets import QStyleOptionViewItem, QWidget

from Api.document_models.studio_documents import StageTemplate
from Api.document_models.project_documents import Stage, Asset
from Gui.mvd.stage_mvd.stage_list_model import StageItemRoles, StageListModel
from Gui.mvd.stage_mvd.stage_list_model import StageItemMetrics
from Gui.mvd.stage_template_mvd.stage_template_list_item_delegate import StageTemplateListItemDelegate
from Gui.popups.status_select_popup import StatusSelectPopup
from Gui.popups.user_browser import UserBrowser

alignment = QtCore.Qt.AlignmentFlag


class StageListItemDelegate(StageTemplateListItemDelegate):
    def __init__(self):
        super().__init__()

    def _set_custom_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        self.stage: Stage = index.data(StageItemRoles.stage)
        self.asset: Asset = self.stage.asset
        self.stage_template: StageTemplate = self.stage.stage_template  # /!\ keep this name the same as in the upper class
        self.can_edit_user = index.data(StageItemRoles.can_edit_user)
        self.can_edit_status = index.data(StageItemRoles.can_edit_status)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem , index: QModelIndex):
        self._set_data(option, index)

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        x, y, w, h = self.get_item_rect()

        self.paint_selected_background(painter)
        self.paint_hover(painter)

        self.paint_logo(painter)
        self.paint_text(painter)

        self.paint_selected_underline(painter)
        self.paint_icon_circle(
            painter,
            icon_path=self.stage.user.icon_path,
            margin=2 if self.can_edit_user else 3,
            offset= [w - StageItemMetrics.status_width - h, 0, 0, 0]
            )
        self.paint_status(painter)

        painter.restore()

    def paint_status(self, painter: QPainter):
        # metrics
        margin = 3 if self.can_edit_status else 4
        x, y, w, h = self.get_item_rect()
        x = w - StageItemMetrics.status_width + margin
        rect = QRect(x, y + margin, StageItemMetrics.status_width - 2 * margin, h - 2 * margin)

        # gui
        text = self.stage.status.label
        pill_color = self.stage.status.color
        text_color = "black"
        font = painter.font()
        if self.can_edit_status:
            font.setPointSizeF(font.pointSizeF() + 0.5)

        painter.save()

        # Paint pill
        painter.setBrush(QBrush(pill_color))
        path = QPainterPath()
        path.addRoundedRect(rect, 3, 3)
        painter.fillPath(path, painter.brush())

        # Paint text
        painter.setPen(text_color)
        painter.setFont(font)
        painter.drawText(rect, text, alignment.AlignHCenter | alignment.AlignVCenter)

        painter.restore()

    # ------------------------
    # Editor
    # ------------------------
    def create_user_editor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        stage: Stage = index.data(StageItemRoles.stage)
        user_browser = UserBrowser(default_user=stage.user)
        return user_browser

    def create_status_editor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        stage: Stage = index.data(StageItemRoles.stage)
        status_editor = StatusSelectPopup()
        return status_editor

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        if index.data(StageItemRoles.can_edit_user):
            editor = self.create_user_editor(parent=parent, option=option, index=index)
        elif index.data(StageItemRoles.can_edit_status):
            editor = self.create_status_editor(parent=parent, option=option, index=index)
        else:
            editor = None

        if editor is not None:
            editor.setWindowFlags(QtCore.Qt.WindowType.Popup)

        self.is_editing = False
        return editor

    def updateEditorGeometry(self, editor, option, index):
        if self.is_editing:
            return

        editor.move(QCursor.pos())
        self.is_editing = True

    def set_user_data(self, editor: UserBrowser, model: StageListModel, index: QModelIndex):
        user = editor.users_list.get_user()
        stage = index.data(StageItemRoles.stage)
        if user is None:
            return
        stage.update(user=user)

    def set_status_data(self, editor: StatusSelectPopup, model: StageListModel, index: QModelIndex):
        stage = index.data(StageItemRoles.stage)
        status = editor.selected_status
        if status is None:
            return
        stage.update(status=status)

    def setModelData(self, editor: UserBrowser | StatusSelectPopup, model: StageListModel, index: QModelIndex):
        if isinstance(editor, UserBrowser):
            self.set_user_data(editor=editor, model=model, index=index)
        elif isinstance(editor, StatusSelectPopup):
            self.set_status_data(editor=editor, model=model, index=index)
        else:
            super().setModelData(editor, model, index)

        model.refresh_view.emit()


class StageListItemDelegateHighlighted(StageListItemDelegate):
    """
    Display a single item that is always highlighted
    """
    def _set_custom_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        super()._set_custom_data(option, index)
        self.opacity = 1
        self.is_hovered = True
        self.is_selected = True

    def paint_hover(self, painter: QPainter):
        return

    def paint_selected_underline(self, painter: QPainter):
        return


class StageListItemDelegateMinimal(StageListItemDelegate):
    """ Don't show user and status infos"""
    def paint(self, painter: QPainter, option: QStyleOptionViewItem , index: QModelIndex):
        self._set_data(option, index)

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.paint_selected_background(painter)
        self.paint_hover(painter)

        self.paint_logo(painter)
        self.paint_text(painter)

        self.paint_selected_underline(painter)

        painter.restore()
