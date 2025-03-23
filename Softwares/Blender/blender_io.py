import bpy

from Softwares.Abstract.abstract_io import AbstractSoftwareFile


class BlenderFile(AbstractSoftwareFile):
    def __init__(self, filepath: str):
        super().__init__(filepath=filepath)

    def open(self):
        bpy.ops.wm.open_mainfile(filepath=self.filepath)

    def save(self):
        # TODO: testing
        #  maybe this should be save_as()
        bpy.ops.wm.save_as_mainfile(filepath=self.filepath)


if __name__ == "__main__":
    import subprocess
    # subprocess.Popen(['Blender', filepath])

    blender_file = BlenderFile(filepath="C:\\Users\marti\OneDrive\Documents\__work\_dev\zephyr_externals\palette.blend")
    blender_file.open()
