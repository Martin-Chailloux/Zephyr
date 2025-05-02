import subprocess


class AbstractSoftwareFile:
    label: str = "Abstract Software"
    exe_path: str = ""

    def __init__(self, filepath: str):
        self.filepath = filepath

    @classmethod
    def open_empty_file(cls):
        print(f"Opening a new {cls.label} file ... ")
        subprocess.Popen([cls.exe_path])

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
