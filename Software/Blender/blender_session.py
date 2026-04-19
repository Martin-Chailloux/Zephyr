import sys
import json
import socket
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Self

class BlenderSession:
    # TODO: editable configs
    # TODO: ship .../modules with Breeze, not compiled
    blender_path = "C:/Program Files/Blender Foundation/Blender 5.0/blender.exe"
    worker_script = "C:/Users/marti/OneDrive/Documents/__work/_dev/Zephyr/Software/Blender/modules/blender_worker.py"
    # worker_script = Path(__file__).with_name("blender_worker.py").resolve()
    # start_up_script: str = Path(__file__).parent.joinpath("startup").joinpath("on_startup.py").resolve()

    def __init__(self, filepath: str, host="127.0.0.1", port=50007, debug: bool=False):
        self.host = host
        self.port = port
        self.proc = None
        self.sock: socket.socket = None
        self.filepath = filepath
        # self.commands = BlenderCommands(session=self)
#         print(f"{self.start_up_script = }")

    def __enter__(self) -> Self:
        print(f"------------------------")
        print(f"Entering Blender Session ...")
        self.proc = subprocess.Popen([
            self.blender_path,
            "-b",
            "--python", self.worker_script,
        ])

        time.sleep(1)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            self.exit()
        except:
            pass

        if self.sock:
            self.sock.close()

        if self.proc:
            self.proc.terminate()

        print("... Blender Session has been exited")
        print(f"------------------------")

    def _send(self, payload: dict):
        # TODO: use a json to be able to send lists
        # tmp_file = Path(tempfile.mkstemp(suffix=".json")[1])
        # tmp_file.write_text(json.dumps(payload))
        # print(f"{tmp_file = }")
        # print(f"{bytes(tmp_file) = }")

        print(f"DEBUG(_send): {payload = }")

        # self.sock.sendall(bytes(tmp_file))
        self.sock.sendall(json.dumps(payload).encode())
        response = json.loads(self.sock.recv(4096).decode())
        # print(f"AZOJE {response = }")

        # tmp_file = str(self.sock.recv(4096))
        # print(f"ALLZEZEZ {tmp_file = }")
        # response = json.loads(tmp_file)
        print(f"DEBUG(_send): {response = }")
        return response


    def _send1(self, payload: dict):
        payload = json.dumps(payload).encode("utf-8")
        self.sock.sendall(payload)
        # print(f"Sending payload ... : {payload = }")

        response = self.sock.recv(4096).decode("utf-8")
#         print(f"... Received answer: {response = }")
        return json.loads(response)

    # ------------------------
    # commands
    # ------------------------
    def exit(self):
        payload = {"name": self.exit.__name__}
        return self._send(payload=payload)

    def test(self):
        payload = {"name": self.test.__name__}
        return self._send(payload=payload)

    def open(self):
        payload = {
            "name": self.open.__name__,
            "filepath": self.filepath,
        }
        return self._send(payload=payload)

    def save(self):
        payload = {
            "name": self.save.__name__,
            "filepath": self.filepath,
        }
        return self._send(payload=payload)

    def save_as(self, filepath: str):
        payload = {
            "name": self.save_as.__name__,
            "filepath": self.filepath,
            "new_filepath": filepath,
        }
        return self._send(payload=payload)

    def get_collections_to_export(self, names: list[str]):
        payload = {
            "name": self.get_collections_to_export.__name__,
            "names": names,
        }
        return self._send(payload=payload)

    def isolate_collection(self, name: str, new_name: str = ""):
        payload = {
            "name": self.isolate_collection.__name__,
            "old_name": name,
            "new_name": new_name,
        }
        return self._send(payload=payload)



