from PySide6 import QtCore
from PySide6.QtCore import QModelIndex, QRect
from PySide6.QtGui import QPainter, QBrush, QPainterPath
from PySide6.QtWidgets import QStyleOptionViewItem

from Api.studio_documents import StageTemplate
from Api.project_documents import Stage, Asset
from Gui.mvd.stage_mvd.stage_list_model import StageItemRoles
from Gui.mvd.stage_mvd.stage_list_model import StageItemMetrics
from Gui.mvd.stage_template_mvd.stage_template_list_item_delegate import StageTemplateListItemDelegate

alignment = QtCore.Qt.AlignmentFlag


class StageListItemDelegate(StageTemplateListItemDelegate):
    def __init__(self):
        super().__init__()

    def _set_custom_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        self.stage: Stage = index.data(StageItemRoles.stage)
        self.asset: Asset = self.stage.asset
        self.stage_template: StageTemplate = self.stage.stage_template  # /!\ keep this name the same as in the upper class
        self.user_is_hovered = index.data(StageItemRoles.user_is_hovered)
        self.status_is_hovered = index.data(StageItemRoles.status_is_hovered)

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
            margin=2 if self.user_is_hovered else 3,
            offset= [w - StageItemMetrics.status_w - h, 0, 0, 0]
            )
        self.paint_status(painter)

        painter.restore()

    def paint_status(self, painter: QPainter):
        # metrics
        margin = 3 if self.status_is_hovered else 4
        x, y, w, h = self.get_item_rect()
        x = w - StageItemMetrics.status_w + margin
        rect = QRect(x, y + margin, StageItemMetrics.status_w - 2 * margin, h - 2 * margin)

        # gui
        text = self.stage.status.label
        pill_color = self.stage.status.color
        text_color = "black"
        font = painter.font()
        if self.status_is_hovered:
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


class StageListItemAlwaysOnDelegate(StageListItemDelegate):
    def _set_custom_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        super()._set_custom_data(option, index)
        self.opacity = 1
        self.is_hovered = True
        self.is_selected = True

    def paint_hover(self, painter: QPainter):
        return

    def paint_selected_underline(self, painter: QPainter):
        return


class StageListMinimalItemDelegate(StageListItemDelegate):
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
