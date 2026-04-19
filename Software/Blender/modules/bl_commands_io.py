import bpy

class BlenderCommandsIo:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def set_filepath(self, filepath: str):
        self.filepath = filepath

    def open(self) -> dict:
        bpy.ops.wm.open_mainfile(filepath=self.filepath)
        return {"status": "ok"}
    
    def save(self) -> dict:
        bpy.ops.wm.save_mainfile(filepath=self.filepath)
        return {"status": "ok"}

    def save_as(self, new_filepath: str) -> dict:
        bpy.ops.wm.save_as_mainfile(filepath=new_filepath)
        self.filepath = new_filepath
        return {"status": "ok"}
