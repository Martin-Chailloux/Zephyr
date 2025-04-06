import qtawesome
from PySide6 import QtCore
from PySide6.QtCore import QModelIndex, QRect, QRectF, QPointF, QPoint
from PySide6.QtGui import QPainter, QBrush, QColor, QPen, QPainterPath, QIcon, QImage, QCursor
from PySide6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QStyle, QListView

from Data.project_documents import Stage, StageTemplate, Asset
from Data.studio_documents import Palette
from Data.status_model import palette
from Gui.stages_widgets.stages_list.stages_list_model import StageItemRoles
from Gui.stages_widgets.stages_list.stages_list_model import StageListItemSizes


alignment = QtCore.Qt.AlignmentFlag


class StageListItemDelegate(QStyledItemDelegate):
    palette: Palette = Palette.objects.get(name="dev")

    def __init__(self, widget: QListView):
        super().__init__()
        self.widget = widget

    def _set_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        self.stage: Stage = index.data(StageItemRoles.stage)
        self.asset: Asset = self.stage.asset
        self.stage_template: StageTemplate = self.stage.stage_template
        self.is_hovered = bool(option.state & QStyle.StateFlag.State_MouseOver)
        self.is_selected = bool(option.state & QStyle.StateFlag.State_Selected)
        self.user_is_hovered = index.data(StageItemRoles.user_is_hovered)
        self.status_is_hovered = index.data(StageItemRoles.status_is_hovered)
        self.opacity: float = 1 if self.is_hovered or self.is_selected else 0.5
        self.item_rect: QRect = option.rect

    def get_item_rect(self) -> (int, int, int, int):
        item_rect = self.item_rect
        return item_rect.x(), item_rect.y()+1, item_rect.width(), item_rect.height()-2

    def paint(self, painter: QPainter, option: QStyleOptionViewItem , index: QModelIndex):
        self._set_data(option, index)

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.paint_selected_background(painter)
        self.paint_hover(painter)

        self.paint_logo(painter)
        self.paint_text(painter)

        self.paint_selected_underline(painter)
        self.paint_user(painter)
        self.paint_status(painter)

        painter.restore()

    def paint_logo(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        margin = 3 if self.is_hovered or self.is_selected else 5

        background_color = self.stage_template.color
        icon_color = self.palette.white_text

        painter.save()

        painter.setOpacity(self.opacity)
        painter.setPen(QColor(0, 0, 0, 0))
        rect = QRectF(x, y, StageListItemSizes.logo_w, h)
        painter.setBrush(QBrush(background_color))
        painter.drawRect(rect)

        painter.setBrush(QBrush(icon_color))
        rect = QRect(x+margin, y+margin, StageListItemSizes.logo_w-2*margin, h-2*margin)
        icon: QIcon = qtawesome.icon(self.stage_template.icon_name, opacity=self.opacity)
        icon.paint(painter, rect, QtCore.Qt.AlignmentFlag.AlignRight)

        painter.restore()

    def paint_text(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        color = QColor(self.palette.white_text)
        padding = 12

        painter.save()
        painter.setOpacity(self.opacity)
        painter.setPen(QPen(color))
        rect = QRect(x + padding + StageListItemSizes.logo_w, y, w, h)
        painter.drawText(rect, self.stage_template.label, alignment.AlignVCenter | alignment.AlignLeft)
        painter.restore()

    def paint_user(self, painter: QPainter):
        margin = 2 if self.user_is_hovered else 4
        x, y, w, h = self.get_item_rect()
        x = w - StageListItemSizes.status_w - h + margin
        rect = QRect(x, y+margin, h-2*margin, h-2*margin)

        icon_path = f"Breeze/Resources/Icons/Users/user_test2.png"
        image = QImage(icon_path)

        painter.save()

        # Set drawing data
        painter.setOpacity(self.opacity)
        painter.setBrush(QBrush(painter.background()))
        painter.setPen(QtCore.Qt.PenStyle.NoPen)

        # Set clip path
        path = QPainterPath(QPointF(x, y))
        path.addEllipse(rect)
        painter.setClipPath(path)

        # Draw image
        painter.drawImage(rect, image)

        painter.restore()

    def paint_status(self, painter: QPainter):
        # metrics
        margin = 2 if self.status_is_hovered else 3
        x, y, w, h = self.get_item_rect()
        x = w - StageListItemSizes.status_w + margin
        rect = QRect(x, y+margin, StageListItemSizes.status_w-2*margin, h-2*margin)

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

    def paint_hover(self, painter: QPainter):
        if not self.is_hovered:
            return

        x, y, w, h = self.get_item_rect()

        painter.save()
        color = QColor(self.palette.white_text)
        color.setAlphaF(0.1)
        painter.setPen(QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(color))
        painter.drawRect(QRectF(QRectF(x, y, w, h)))
        painter.restore()

    def paint_selected_background(self, painter: QPainter):
        if not self.is_selected:
            return

        x, y, w, h = self.get_item_rect()
        color = QColor(self.palette.white_text)
        color.setAlphaF(0.2)

        painter.save()

        painter.setPen(QPen(QColor(0, 0, 0, 0)))
        painter.setBrush(QBrush(color))
        painter.drawRect(x, y, w, h)

        painter.restore()

    def paint_selected_underline(self, painter: QPainter):
        if not self.is_selected:
            return

        x, y, w, h = self.get_item_rect()
        color = self.palette.green
        height = 2

        painter.save()

        painter.setPen(QPen(QColor(0, 0, 0, 0)))
        painter.setBrush(QBrush(color))
        painter.drawRect(QRectF(x, y+h-height, w, height))

        painter.restore()
