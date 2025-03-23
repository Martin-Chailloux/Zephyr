from dataclasses import dataclass

from PySide6.QtGui import QIcon, QPixmap


@dataclass
class SoftwareModel:
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
class Software:
    krita = SoftwareModel(   label="Krita",    icon_path="Breeze/Resources/Icons/Software/krita.png")
    maya = SoftwareModel(    label="Maya",     icon_path="Breeze/Resources/Icons/Software/maya.png")
    blender = SoftwareModel( label="Blender",  icon_path="Breeze/Resources/Icons/Software/blender.png")
    guerilla = SoftwareModel(label="Guerilla", icon_path="Breeze/Resources/Icons/Software/guerilla.png")
    nuke = SoftwareModel(    label="Nuke",     icon_path="Breeze/Resources/Icons/Software/nuke.png")
