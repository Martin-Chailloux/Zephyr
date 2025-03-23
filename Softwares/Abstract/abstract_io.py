

class AbstractSoftwareFile:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def open(self):
        pass

    def save(self):
        pass