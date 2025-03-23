import subprocess
import bpy

from Softwares.Abstract.abstract_io import AbstractSoftwareFile


class BlenderFile(AbstractSoftwareFile):
    exe_path: str = "C:/Program Files/Blender Foundation/Blender 4.3/blender-launcher.exe"
    
    def __init__(self, filepath: str):
        super().__init__(filepath=filepath)

    def open_interactive(self):
        subprocess.Popen([self.exe_path, self.filepath])

    def open(self):
        bpy.ops.wm.open_mainfile(filepath=self.filepath)

    def save(self):
        bpy.ops.wm.save_mainfile(filepath=self.filepath)

    def save_as(self, filepath: str):
        # TODO: testing
        self.filepath = filepath
        bpy.ops.wm.save_as_mainfile(filepath=self.filepath)


if __name__ == "__main__":
    blender_file = BlenderFile(filepath="C:/Users/marti/OneDrive/Documents/__work/_dev/zephyr_externals/palette.blend")

    blender_file.open()

    # test: create collection
    collection = bpy.data.collections.new("MyTestCollection")
    bpy.context.scene.collection.children.link(collection)
    # ------------------------

    blender_file.save()
    blender_file.open_interactive()
