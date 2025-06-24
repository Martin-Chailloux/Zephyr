import socket
import json

from blender_file import BlenderFile


def ask(command, **kwargs) -> json:
    data = {
        "software": "Blender",
        "command": command,
        "params": kwargs or {},
    }

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", BlenderFile.port))
        s.sendall(json.dumps(data).encode("utf-8"))
        data=s.recv(1024)
        print(f"{data = }")
