"""
Back and forth instructions between Blender and Breeze:
 - simple command + json data
 - Blender should never know about Breeze's modules
"""

import bl_dialog


def save_inc(source_filepath: str) -> str:
    new_filepath = bl_dialog.ask(command="save_inc", source_filepath=source_filepath)
    return new_filepath

# # pseudocode:
# class SaveInc:
#     command = "save_inc"
#
#     @classmethod
#     def to_breeze(cls, source_filepath: str):
#
#     @classmethod
#     def to_blender(cls, target_filepath: str):
#         pass

# if __name__ == '__main__':
#     SaveInc.to_breeze(source_filepath="where/should/i/save/myself")
