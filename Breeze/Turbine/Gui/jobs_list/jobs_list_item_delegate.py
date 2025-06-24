from PySide6 import QtCore
from PySide6.QtCore import QModelIndex, QRect
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QStyleOptionViewItem

from Data.project_documents import MgJob
from Gui.GuiWidgets.abstract_widgets.abstract_mvd import AbstractListDelegate
from Turbine.Gui.jobs_list.jobs_list_model import JobItemRoles, JobItemMetrics

alignment = QtCore.Qt.AlignmentFlag


class JobsListItemDelegate(AbstractListDelegate):
    def __init__(self):
        super().__init__()

    def _set_custom_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        self.job: MgJob = index.data(JobItemRoles.job)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem , index: QModelIndex):
        self._set_data(option, index)

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.paint_selected_background(painter)
        self.paint_hover(painter)
        self.paint_selected_underline(painter)

        self.paint_icon_circle(painter, icon_path=self.job.user.icon_path, offset=[2, 2,-4, -4])
        self.paint_version_num(painter)
        self.paint_label(painter)
        self.paint_context(painter)
        x, y, w, h = self.get_item_rect()
        self.paint_time(painter, time=self.job.creation_time, rect=QRect(w - JobItemMetrics.datetime_w, y, JobItemMetrics.datetime_w, h))

        painter.restore()

    def paint_version_num(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        color = QColor(self.palette.white_text)

        painter.save()
        painter.setPen(QPen(color))

        rect = QRect(x + JobItemMetrics.user_w, y, JobItemMetrics.user_w, h)
        text = f"v{self.job.source_version.number:03d}"
        painter.drawText(rect, text, alignment.AlignLeft | alignment.AlignVCenter)

        painter.restore()

    def paint_label(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        color = QColor(self.palette.white_text)

        painter.save()
        painter.setPen(QPen(color))

        rect = QRect(x + JobItemMetrics.version_w, y, w, h/2)
        text = self.job.source_process.label
        painter.drawText(rect, text, alignment.AlignLeft | alignment.AlignBottom)

        painter.restore()

    def paint_context(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        y -= 2

        color = QColor(self.palette.white_text)

        stage = self.job.source_version.collection.stage
        asset = stage.asset

        painter.save()

        painter.setPen(QPen(color))
        font = painter.font()
        font.setPointSizeF(self.medium_font_size)
        painter.setFont(font)
        painter.setOpacity(self.opacity)

        rect = QRect(x + JobItemMetrics.version_w, y + h/2, w, h/2)
        text = f"{asset.category} > {asset.name} > {asset.variant} > {stage.stage_template.label}"
        painter.drawText(rect, text, alignment.AlignLeft | alignment.AlignTop)

        painter.restore()
