from Api.project_documents import Version, Stage
from Gui.components.popups.software_select_menu import CommentEditMenu, SoftwareSelectMenu


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
    version = stage.work_component.create_last_version(software=software_select.software)
    version.update(comment=comment_box.comment)

    # create file
    file = version.to_file()
    file.new_file()
    print(f"Created file: {file.filepath}")


# TODO: Version.increment()
def increment(old_version: Version):
    comment_box = CommentEditMenu(title="Comment: ", default_comment=f"Increment from v{old_version.number:03d}")
    confirm = comment_box.exec()

    if not confirm:
        return

    # reserve version
    new_version = old_version.component.create_last_version(software=old_version.software)
    new_version.update(comment=comment_box.comment)

    # create file
    file = old_version.to_file()
    file.save_as(filepath=new_version.filepath)
