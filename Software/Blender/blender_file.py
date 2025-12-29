import sys

# externalize logs
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

import subprocess
import threading
import bpy

from software_base import AbstractSoftwareFile


class BlenderFile(AbstractSoftwareFile):
    label: str = "Blender"
    exe_path: str = "C:/Program Files/Blender Foundation/Blender 4.3/blender.exe"
    port = 9000
    start_up_script: str = "C:/Users/marti/OneDrive/Documents/__work/_dev/Zephyr/Software/Blender/startup/on_startup.py"
    
    def __init__(self, filepath: str):
        super().__init__(filepath=filepath)

    def _open_interactive(self):
        # env = os.environ.copy()
        # env["PYTHONUNBUFFERED"] = "1"  # not needed, delete later (with env=env below)

        process = subprocess.Popen(
            # [self.exe_path, self.filepath, "--debug-python", self.start_up_script],  # TODO: ca crash (utiliser logging a la place pour prints dans draw() etc)
            [self.exe_path, self.filepath, "--python", self.start_up_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            # env=env,   # not needed, delete later
        )
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            elif line:
                print("[Blender]", line.strip())

    def open_interactive(self):
        # TODO: @as_thread
        threading.Thread(target=self._open_interactive, daemon=False).start()

    def open(self):
        # if this is not called the code still works, but it is done from the default file
        bpy.ops.wm.open_mainfile(filepath=self.filepath)

    def save(self):
        bpy.ops.wm.save_mainfile(filepath=self.filepath)

    def save_as(self, filepath):
        bpy.ops.wm.save_as_mainfile(filepath=filepath)
        self.set_filepath(filepath)

    def new_file(self):
        bpy.ops.wm.read_homefile()
        self.save()

    def test(self):
        print(f"TEST")
        bpy.data.objects['Cube'].location[0] = 5


if __name__ == "__main__":
    blender_file = BlenderFile(filepath="C:/Users/marti/OneDrive/Documents/__work/_dev/zephyr_externals/palette.blend")

    blender_file.open()

    # test: create collection
    collection = bpy.data.components.new("MyTestCollection")
    bpy.context.scene.version.children.link(collection)
    # ------------------------

    blender_file.save()
    blender_file.open_interactive()
