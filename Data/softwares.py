from PySide6.QtGui import QIcon


class Software:
    label: str
    icon_path: str
    is_enabled: bool = True

    @property
    def icon(self) -> QIcon:
        icon = QIcon()
        icon.addFile(self.icon_path)
        return icon


class Krita(Software):
    label: str = "Krita"
    icon_path: str = "Icons/Softwares/krita.png"
    is_enabled: bool = False


class Maya(Software):
    label: str = "Maya"
    icon_path: str = "Icons/Softwares/maya.png"
    is_enabled: bool = False


class Blender(Software):
    label: str = "Blender"
    icon_path: str = "Icons/Softwares/blender.png"


class GuerillaRender(Software):
    label: str = "Guerilla Render"
    icon_path: str = "Icons/Softwares/guerilla_render.png"


class Nuke(Software):
    label: str = "Nuke"
    icon_path: str = "Icons/Softwares/nuke.png"
