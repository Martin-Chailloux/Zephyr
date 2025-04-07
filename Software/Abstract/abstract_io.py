

class AbstractSoftwareFile:
    exe_path: str = ""

    def __init__(self, filepath: str):
        self.filepath = filepath

    def open_interactive(self):
        pass

    def open(self):
        pass

    def save(self):
        pass

    def save_as(self, filepath: str):
        pass
