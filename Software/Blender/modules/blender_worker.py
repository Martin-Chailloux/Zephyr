import sys
import tempfile
from pathlib import Path

import bpy
import socket
import json

from bl_commands import BlenderCommands


HOST = "127.0.0.1"
PORT = 50007


class BlenderWorker:
    def __init__(self):
        # if False:  # debug on/off
        #     sys.stdout.reconfigure(line_buffering=True)
        #     sys.stderr.reconfigure(line_buffering=True)

        self.payload = None
        self.filepath = ""
        self.commands = BlenderCommands(filepath=self.filepath)

    def receive(self, payload: dict) -> dict:
        self.payload = payload
        self.filepath = payload.get('filepath', "")
        self.commands.set_filepath(filepath=self.filepath)

        name: str = payload.get('name', '')
        command = getattr(self, name, None)
        if command is None:
            raise NotImplementedError(f"Command: {name}")
        else:
            print(f"Running command '{command.__name__}' ... ")
            result = command()
            print(f"... {result = }")
            return result

    # ------------------------
    # commands
    # ------------------------
    def open(self):
        return self.commands.io.open()

    def save(self):
        return self.commands.io.save()

    def save_as(self):
        new_filepath = self.payload.get('new_filepath', self.filepath)
        return self.commands.io.save_as(new_filepath=new_filepath)

    def test(self):
        bpy.ops.mesh.primitive_monkey_add()
        return {"status": "ok"}

    def get_collections_to_export(self):
        names = self.payload.get("names", "")
        return self.commands.export.get_collections(component_names=names)

    def isolate_collection(self):
        name = self.payload.get("old_name", "")
        new_name = self.payload.get("new_name", "")
        return self.commands.export.isolate_collection(name=name, new_name=new_name)

    def exit(self):
        return {"status": "exit"}


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(1)

    connection, addr = sock.accept()

    while True:
        # tmp_file = str(connection.recv(4096))
        # if not tmp_file:
        #     break
        # payload = json.loads(tmp_file)

        payload = json.loads(connection.recv(4096).decode())

        # payload = json.loads(data.decode("utf-8"))
        result: dict = BlenderWorker().receive(payload)
        # tmp_file = Path(tempfile.mkstemp(suffix=".json")[1])
        # tmp_file.write_text(json.dumps(result))
        # connection.sendall(bytes(tmp_file))
        connection.sendall(json.dumps(result).encode())
        if result.get('status', None) == "exit":
            break

    connection.close()
    sock.close()


def main2():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(1)

    connection, addr = sock.accept()

    while True:
        data = connection.recv(4096)
        if not data:
            break

        payload = json.loads(data.decode("utf-8"))
        result = BlenderWorker().receive(payload)
        connection.sendall(json.dumps(result).encode("utf-8"))
        if result.get('status', None) == "exit":
            break

    connection.close()
    sock.close()


if __name__ == "__main__":
    main()
