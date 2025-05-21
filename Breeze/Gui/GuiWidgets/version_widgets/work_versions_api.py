from Data import breeze_converters
from Data.project_documents import Version, Stage
from Gui.GuiWidgets.software_widgets.software_select_menu import CommentEditMenu, SoftwareSelectMenu


def new_empty_version(stage: Stage):
    software_select = SoftwareSelectMenu(stage=stage)
    confirm = software_select.exec()
    if not confirm:
        return
    elif software_select.software is None:
        return

    comment_box = CommentEditMenu(title="Comment: ", default_comment="New file")
    confirm = comment_box.exec()
    if not confirm:
        return

    # reserve version
    version = stage.work_collection.create_last_version(software_select.software)
    version.update(comment=comment_box.comment)

    # create file
    software_instance = breeze_converters.get_file_instance_from_software(software=software_select.software,
                                                                          filepath=version.filepath)
    software_instance.new_file()
    print(f"Created file: {software_instance.filepath}")


def increment(old_version: Version):
    comment_box = CommentEditMenu(title="Comment: ", default_comment=f"Increment from v{old_version.number:03d}")
    confirm = comment_box.exec()

    if not confirm:
        return

    # reserve version
    new_version = old_version.collection.create_last_version(software=old_version.software)
    new_version.update(comment=comment_box.comment)

    # create file
    software_instance = breeze_converters.get_file_instance_from_software(software=new_version.software,
                                                                          filepath=old_version.filepath)
    software_instance.save_as(filepath=new_version.filepath)
