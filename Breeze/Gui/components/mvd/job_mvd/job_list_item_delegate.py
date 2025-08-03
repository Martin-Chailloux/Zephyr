import qtawesome
from PySide6 import QtCore
from PySide6.QtCore import QModelIndex, QRect, QPoint
from PySide6.QtGui import QPainter, QColor, QPen, QFontMetrics, QIcon
from PySide6.QtWidgets import QStyleOptionViewItem

from Api.breeze_app import BreezeApp
from Api.project_documents import Job
from Api.turbine.step import StepBase
from Gui.components.mvd.abstract_mvd import AbstractListDelegate
from Gui.components.mvd.job_mvd.job_list_model import JobItemRoles, JobItemMetrics


alignment = QtCore.Qt.AlignmentFlag


class JobListItemDelegate(AbstractListDelegate):
    def __init__(self):
        super().__init__()

    def _set_custom_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        self.job: Job = index.data(JobItemRoles.job)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem , index: QModelIndex):
        self._set_data(option, index)

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.paint_selected_background(painter)
        self.paint_hover(painter)
        self.paint_selected_underline(painter)

        self.paint_icon_circle(painter, icon_path=self.job.user.icon_path, offset=[4, 4, -8, -8])
        self.paint_job_pill(painter)
        self.paint_job_label(painter)
        self.paint_task_context(painter)
        x, y, w, h = self.get_item_rect()
        self.paint_time(painter, time=self.job.creation_time, rect=QRect(w - JobItemMetrics.datetime_w, y, JobItemMetrics.datetime_w, h))

        painter.restore()

    def paint_job_label(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        x += JobItemMetrics.user_w
        y += h/2
        color = QColor(BreezeApp.palette.white_text)

        painter.save()

        painter.setPen(QPen(color))
        rect = QRect(x, y, w, h)
        text = self.job.source_process.label
        painter.drawText(rect, text, alignment.AlignLeft | alignment.AlignTop)

        painter.restore()

    def paint_job_pill(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        x += JobItemMetrics.user_w
        y += h/2 - JobItemMetrics.pill_wh

        main_step = StepBase.from_dict(infos=self.job.steps)
        icon: QIcon = qtawesome.icon(main_step.pill.icon_name, color=main_step.pill.color)
        pixmap = icon.pixmap(int(JobItemMetrics.pill_wh))

        painter.save()
        painter.drawPixmap(QPoint(x, y), pixmap)
        painter.restore()

    def paint_task_context(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        x += + JobItemMetrics.user_w + JobItemMetrics.label_w

        stage = self.job.source_version.component.stage
        asset = stage.asset

        painter.save()

        # version num
        painter.setPen(QPen(BreezeApp.palette.white_text))
        rect = QRect(x, y, w, h/2)
        text = f"{self.job.source_version.number:03d} - "
        painter.setPen(QPen(BreezeApp.palette.white_text))
        painter.drawText(rect, text, alignment.AlignLeft | alignment.AlignBottom)

        # task template
        font_metrics = QFontMetrics(painter.font())
        text_w = font_metrics.horizontalAdvance(text)

        painter.setPen(QPen(stage.stage_template.color))
        rect = QRect(x + text_w, y, w, h/2)
        text = f"{stage.stage_template.label}"
        painter.drawText(rect, text, alignment.AlignLeft | alignment.AlignBottom)

        # asset path
        font = painter.font()
        font.setPointSizeF(self.medium_font_size)
        painter.setFont(font)
        painter.setOpacity(self.opacity)

        painter.setPen(QPen(BreezeApp.palette.white_text))
        rect = QRect(x, y + h/2, w, h/2)
        text = f"{asset.category} ⮞ {asset.name} ⮞ {asset.variant}"
        painter.drawText(rect, text, alignment.AlignLeft | alignment.AlignTop)

        painter.restore()
