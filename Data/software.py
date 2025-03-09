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
    krita = SoftwareModel(   label="Krita",    icon_path="Resources/Icons/Softwares/krita.png")
    maya = SoftwareModel(    label="Maya",     icon_path="Resources/Icons/Softwares/maya.png")
    blender = SoftwareModel( label="Blender",  icon_path="Resources/Icons/Softwares/blender.png")
    guerilla = SoftwareModel(label="Guerilla", icon_path="Resources/Icons/Softwares/guerilla.png")
    nuke = SoftwareModel(    label="Nuke",     icon_path="Resources/Icons/Softwares/nuke.png")
