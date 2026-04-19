import json
import sys
import tempfile
from pathlib import Path

# from Software.Blender.blender_file_worker import BlenderActions

# # externalize logs
# sys.stdout.reconfigure(line_buffering=True)
# sys.stderr.reconfigure(line_buffering=True)

import subprocess
import threading

from Software.Abstract.software_base import AbstractSoftwareFile



class BlenderFile(AbstractSoftwareFile):
    label: str = "Blender"
    exe_path: str = "C:/Program Files/Blender Foundation/Blender 5.0/blender.exe"
    port = 9000
    start_up_script: str = "C:/Users/marti/OneDrive/Documents/__work/_dev/Zephyr/Software/Blender/startup_interactive/create_menu.py"
    
    def __init__(self, filepath: str):
        super().__init__(filepath=filepath)
        self.worker_script = Path(__file__).with_name("blender_server.py")

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
        # while True:
        #     line = process.stdout.readline()
        #     if not line and process.poll() is not None:
        #         break
        #     elif line:
        #         print("[Blender]", line.strip())

    def open_interactive(self):
        # TODO: @as_thread
        threading.Thread(target=self._open_interactive, daemon=False).start()

    def run_background(self, action: str, payload: dict = None):
        payload = payload or {}
        payload[action] = action

        # Write payload to a temporary JSON file
        tmp_file = Path(tempfile.mkstemp(suffix=".json")[1])
        tmp_file.write_text(json.dumps(payload))

        print(f"Sending request to blender worker ... {action = }, {payload = }")

        subprocess.run([
            str(self.exe_path),
            "--background",
            "--python", str(self.worker_script),
            "--",
            str(tmp_file)
        ])

    def open(self):
        import bpy
        # # if this is not called the code still works, but it is done from the default file
        bpy.ops.wm.open_mainfile(filepath=self.filepath)
        # self.run_background(action=BlenderActions.open)

    def save(self):
        import bpy
        bpy.ops.wm.save_mainfile(filepath=self.filepath)
        # self.run_background(action=BlenderActions.save)

    def save_as(self, filepath):
        import bpy

        bpy.ops.wm.save_as_mainfile(filepath=filepath)
        self.set_filepath(filepath)
        # payload = {"target_path": filepath}
        # self.run_background(action=BlenderActions.save_as, payload=payload)


    def new_file(self):
        import bpy
        bpy.ops.wm.read_homefile()
        self.save()
        # self.run_background(action=BlenderActions.new_file)

    def test(self):
        print(f"TEST")
        # bpy.data.objects['Cube'].location[0] = 5


if __name__ == "__main__":
    blender_file = BlenderFile(filepath="C:/Users/marti/OneDrive/Documents/__work/_dev/zephyr_externals/palette.blend")

    blender_file.open()

    # test: create collection
    # collection = bpy.data.components.new("MyTestCollection")
    # bpy.context.scene.version.children.link(collection)
    # ------------------------

    blender_file.save()
    blender_file.open_interactive()
