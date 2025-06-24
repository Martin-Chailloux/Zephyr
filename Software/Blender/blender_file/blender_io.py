import bpy

# TODO: bpy.types.collection does not exist
#  bpy.types has no typing

class BlenderIo:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def export_blend(self, collection):
        pass

    def export_abc(self, collection):
        pass