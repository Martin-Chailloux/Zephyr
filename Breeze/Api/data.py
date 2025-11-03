

class _DataNamesBase:
    @classmethod
    def all(cls) -> list[str]:
        return []


class Categories(_DataNamesBase):
    character = "Character"
    decor = "Decor"
    element = "Element"
    library = "Library"
    prop = "Prop"
    sandbox = "Sandbox"
    sequence = "Sequence"
    templates = "Templates"

    @classmethod
    def all(cls) -> list[str]:
        return [cls.character, cls.decor, cls.element, cls.library,
                cls.prop, cls.sandbox, cls.sequence, cls.templates]


class StageTemplates(_DataNamesBase):
    modeling = "modeling"
    rigging = "rigging"
    texturing = "texturing"
    shading = "shading"
    animation = "animation"
    lighting = "lighting"

    @classmethod
    def all(cls) -> list[str]:
        return [cls.modeling, cls.rigging, cls.texturing, cls.shading,
                cls.animation, cls.lighting]


class Components(_DataNamesBase):
    work = "work"
    geo = "geo"
    rig = "rig"
    cam_rig = "camrig"
    light_rig = "lightrig"
    shd = "shd"
    cam = "cam"
    anim = "anim"
    review = "review"

    @classmethod
    def all(cls) -> list[str]:
        return [cls.geo, cls.rig, cls.review]


class Softwares(_DataNamesBase):
    blender = "blender"


class Templates(_DataNamesBase):
    build = "build"
    export = "export"
    review = "review"


class Extensions(_DataNamesBase):
    jpg = "jpg"
    png = "png"
    exr = "exr"

    blend = "blend"
    ma = "ma"
