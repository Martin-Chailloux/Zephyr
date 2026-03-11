from PySide6 import QtCore
from PySide6.QtCore import QModelIndex, QRect
from PySide6.QtGui import QPainter, QColor, QPen, QFontMetrics, QImage
from PySide6.QtWidgets import QStyleOptionViewItem

from Breeze.Api.breeze_app import BreezeApp
from Breeze.Api.document_models.studio_documents import Project
from Breeze.Gui.mvd.abstract_mvd import AbstractItemDelegate
from Breeze.Gui.mvd.project_mvd.project_list_model import ProjectItemRoles, ProjectItemMetrics

alignment = QtCore.Qt.AlignmentFlag


class ProjectListItemDelegate(AbstractItemDelegate):
    def __init__(self):
        super().__init__()

    def _set_custom_data(self, option: QStyleOptionViewItem, index: QModelIndex):
        self.project: Project = index.data(ProjectItemRoles.project)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem , index: QModelIndex):
        self._set_data(option, index)

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.paint_selected_background(painter)
        self.paint_hover(painter)
        self.paint_thumbnail(painter)
        self.paint_selected_underline(painter)
        self.paint_text(painter)

        painter.restore()

    def paint_text(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        color = QColor(BreezeApp.palette.white_text)
        padding = 5
        x += padding

        painter.save()

        painter.setPen(QPen(color))

        text = f"{self.project.name} "
        rect = QRect(x, y, w, h)
        painter.drawText(rect, text, alignment.AlignLeft | alignment.AlignVCenter)

        painter.restore()

    def paint_thumbnail(self, painter: QPainter):
        x, y, w, h = self.get_item_rect()
        image = QImage(self.project.thumbnail_path)
        if image.isNull():
            return

        painter.save()

        # TODO: this only work with 16/9 images, either force the ratio when creating thumbnails or improve this
        img_height = ProjectItemMetrics.height - 2
        img_width = 16/9 * img_height
        x = w - img_width

        rect = QRect(x, y, int(img_width), int(img_height))
        painter.drawImage(rect, image)

        painter.restore()
