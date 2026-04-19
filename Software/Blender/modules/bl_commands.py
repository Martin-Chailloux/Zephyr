from bl_commands_export import BlenderCommandsExport
from bl_commands_io import BlenderCommandsIo


class BlenderCommands:
    def __init__(self, filepath: str):
        self.io = BlenderCommandsIo(filepath=filepath)
        self.export = BlenderCommandsExport()

    def set_filepath(self, filepath: str):
        self.io.set_filepath(filepath=filepath)