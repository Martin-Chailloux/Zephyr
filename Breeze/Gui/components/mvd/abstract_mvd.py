import datetime

from PySide6 import QtCore
from PySide6.QtCore import QPoint, QModelIndex, QRect, QRectF, QPointF
from PySide6.QtGui import (QCursor, QStandardItem, QStandardItemModel, QPainter, QColor,
                           QBrush, QPen, QImage, QPainterPath)
from PySide6.QtWidgets import QListView, QStyledItemDelegate, QStyleOptionViewItem, QStyle

from Api.breeze_app import BreezeApp


alignment = QtCore.Qt.AlignmentFlag


class AbstractListView(QListView):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self._model: QStandardItemModel = None

    def _connect_signals(self):
        pass

    def _get_viewport_rect(self) -> (int, int, int, int):
        rect = self.viewport().rect()
        return rect.x(), rect.y(), rect.width(), rect.height()

    def _get_mouse_pos(self) -> QPoint:
        position: QPoint = self.mapFromGlobal(QCursor.pos())
        return position

    def _get_hovered_index(self) -> QModelIndex:
        mouse_pos = self._get_mouse_pos()
        index = self.indexAt(mouse_pos)
        return index

    def get_hovered_item(self) -> QStandardItem:
        hovered_index = self._get_hovered_index()
        hovered_item = self._model.item(hovered_index.row())
        return hovered_item

    def get_selected_items(self) -> list[QStandardItem]:
        selected_indexes = self.selectionModel().selectedIndexes()
        selected_items = [self._model.item(index.row()) for index in selected_indexes]
        return selected_items

    def select_row(self, row: int):
        index = self._model.index(row, 0)
        self.setCurrentIndex(index)


class AbstractListModel(QStandardItemModel):
    def __init__(self):
        super().__init__()

    def add_item(self, **kwargs):
        pass

    @property
    def items(self):
        items = [self.item(row) for row in range(self.rowCount())]
        return items

    def refresh(self):
        return


class AbstractListDelegate(QStyledItemDelegate):
    small_font_size: int = 7
    medium_font_size: int = 8
    palette = BreezeApp.palette

    def __init__(self):
        super().__init__()

    def _set_common_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        self.is_hovered = bool(option.state & QStyle.StateFlag.State_MouseOver)
        self.is_selected = bool(option.state & QStyle.StateFlag.State_Selected)
        self.item_rect: QRect = option.rect
        self.opacity: float = 1 if self.is_hovered or self.is_selected else 0.5

    def _set_custom_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        pass

    def _set_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        self._set_common_data(option, index)
        self._set_custom_data(option, index)

    def get_item_rect(self) -> (int, int, int, int):
        item_rect = self.item_rect
        return item_rect.x(), item_rect.y()+1, item_rect.width(), item_rect.height()-2

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

    def paint_icon_circle(self, painter: QPainter, icon_path: str, margin: int=2, offset: list[int] = None, rect: QRect = None):
        x, y, w, h = self.get_item_rect()
        offset = offset or [0, 0, 0, 0]
        if len(offset) != 4:
            raise ValueError("Could not read offset, should be: [x, y, w, h]")
        rect = rect or QRect(x+margin+offset[0], y+margin+offset[1], h-2*margin+offset[2], h-2*margin+offset[3])

        image = QImage(icon_path)

        painter.save()

        # Set drawing data
        painter.setOpacity(self.opacity)
        painter.setBrush(QBrush(painter.background()))
        painter.setPen(QtCore.Qt.PenStyle.NoPen)

        # Set clip path
        icon_path = QPainterPath(QPointF(x, y))
        icon_path.addEllipse(rect)
        painter.setClipPath(icon_path)

        # Draw image
        painter.drawImage(rect, image)

        painter.restore()

    def paint_time(self, painter: QPainter, time: datetime, rect: QRect=None):
        if rect is None:
            x, y, w, h = self.get_item_rect()
        else:
            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()

        time_text = f"{time.hour:02d}h{time.minute:02d}"
        date_text = f"{time.day:02d}/{time.month:02d}/{time.year:04d}"

        painter.save()
        painter.setOpacity(self.opacity)
        font = painter.font()
        font.setPointSizeF(self.small_font_size)
        painter.setFont(font)

        # paint time
        rect = QRect(x, y, w, h/2)
        painter.drawText(rect, time_text, alignment.AlignHCenter | alignment.AlignBottom)

        # paint date
        rect = QRect(x, y + h/2, w, h/2)
        painter.drawText(rect, date_text, alignment.AlignHCenter | alignment.AlignTop)
        painter.restore()
