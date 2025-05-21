from Data.studio_documents import Software
from blender_io import BlenderFile


def get_file_instance_from_software(software: Software, filepath: str):
    if software.label == 'Blender':
        return BlenderFile(filepath=filepath)
    else:
        raise NotImplementedError(f"File instance for: {software.__repr__()}")

class BreezeText:
    def __init__(self, text: str):
        self.text = text

        # TODO: def is_valid() to have the logic here rather than elsewhere

    def to_valid_name(self):
        split_text = self.text.replace("_", " ").replace("-", " ").split()
        if len(split_text) == 0:
            return self.text
        else:
            return split_text[0] + "".join(s.replace(s[0], s[0].upper()) for s in split_text[1:])
