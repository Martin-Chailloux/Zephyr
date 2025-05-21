import subprocess


class AbstractSoftwareFile:
    label: str = "Abstract Software"
    exe_path: str = ""
    port: int = 9999

    def __init__(self, filepath: str):
        self.filepath = filepath

    def set_filepath(self, filepath: str):
        self.filepath = filepath

    def open_interactive(self):
        pass

    def open(self):
        pass

    def save(self):
        pass

    def save_as(self, filepath: str = None):
        pass

    def new_file(self):
        pass
