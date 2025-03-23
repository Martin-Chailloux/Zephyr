from dataclasses import dataclass

from PySide6.QtGui import QIcon, QPixmap


@dataclass
class SoftwareItem:
    label: str
    icon_path: str
    is_enabled: bool = True

    @property
    def icon(self):
        icon = QIcon()
        icon.addFile(self.icon_path)
        return icon

    @property
    def pixmap(self):
        pixmap = QPixmap(self.icon_path)
        return pixmap


@dataclass
class SoftwareModel:
    krita = SoftwareItem(label="Krita", icon_path="Breeze/Resources/Icons/Software/krita.png")
    maya = SoftwareItem(label="Maya", icon_path="Breeze/Resources/Icons/Software/maya.png")
    blender = SoftwareItem(label="Blender", icon_path="Breeze/Resources/Icons/Software/blender.png")
    guerilla = SoftwareItem(label="Guerilla", icon_path="Breeze/Resources/Icons/Software/guerilla.png")
    nuke = SoftwareItem(label="Nuke", icon_path="Breeze/Resources/Icons/Software/nuke.png")
