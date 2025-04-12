import subprocess


class AbstractSoftwareFile:
    label: str = "Abstract Software"
    exe_path: str = ""

    def __init__(self, filepath: str):
        self.filepath = filepath

    def open_interactive(self):
        pass

    @classmethod
    def new_file(cls):
        print(f"Opening a new {cls.label} file ... ")
        subprocess.Popen([cls.exe_path])

    def open(self, interactive: bool=False):
        pass

    def save(self):
        pass

    def save_as(self, filepath: str):
        pass
