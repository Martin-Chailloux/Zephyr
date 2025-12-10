from Api.document_models.project_documents import Version, Stage
from Gui.popups.software_browser import CommentEditMenu, SoftwareBrowser


def create_empty_version(stage: Stage) -> bool:
    software_browser = SoftwareBrowser(stage=stage)
    confirm = software_browser.show_menu(position=[0.5, 0.25])
    if not confirm:
        return False
    software = software_browser.software_list.get_software()

    comment_box = CommentEditMenu(title="Comment: ", default_comment="New file")
    confirm = comment_box.show_menu(position=[0.5, 0.3])
    if not confirm:
        return False

    # create version
    if stage.get_work_component() is None:
        stage.create_work_component(extension=software.extension)
        stage.reload()
    version = stage.get_work_component().create_last_version(software=software)
    version.update(comment=comment_box.comment)

    # create file
    file = version.to_file()
    file.new_file()
    print(f"Created file: {file.filepath}")
    return True

def increment(old_version: Version) -> bool:
    comment_box = CommentEditMenu(title="Comment: ", default_comment=f"Increment from v{old_version.number:03d}")
    confirm = comment_box.show_menu(position=[0.5, 0.3])
    if not confirm:
        return False

    # create version
    new_version = old_version.increment(comment=comment_box.comment)

    # create file
    file = old_version.to_file()
    file.save_as(filepath=new_version.filepath)
    return True


def edit_comment(version: Version) -> bool:
    comment_box = CommentEditMenu(title="Comment: ", default_comment=version.comment)
    confirm = comment_box.show_menu(position=[0.5, 0.3])
    if not confirm:
        return False

    version.update(comment=comment_box.comment)

    return True