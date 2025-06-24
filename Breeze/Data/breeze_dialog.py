import json
import socket
import threading

from Data.studio_documents import StageTemplate
from blender_file import BlenderFile

ports = [
    BlenderFile.port
]


class Listener:
    def __init__(self):
        # TODO: what does args do exactly ?
        threading.Thread(target=self.listen, args=(BlenderFile.port,), daemon=True).start()

    def listen(self, data: int):
        print(f"LISTENING FOR SOFTWARES REQUEST ...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            for port in ports:
                s.bind(("localhost", port))
            s.listen(len(ports))

            connection, address = s.accept()
            with connection:
                print('Connected by', address)
                while True:
                    data = connection.recv(1024)
                    if not data: break
                    data = self.convert_data(data)
                    connection.sendall(data)


    def convert_data(self, data: json) -> json:
        # TODO: should be in the software's repo ?
        # or: this dispatch the data to specialized sub classes in the software's repos
        print(f"RECEIVED: {data = }")
        data = json.loads(data)

        data["It is working !!"] = True
        stage_templates = StageTemplate.objects()
        # data["stage_templates"] = stage_templates.to_json()

        return json.dumps(data).encode("utf-8")
