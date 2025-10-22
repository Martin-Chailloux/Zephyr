from Api.document_models.project_documents import Version, Stage
from Gui.popups.software_browser import CommentEditMenu, SoftwareBrowser


def new_empty_version(stage: Stage):
    software_browser = SoftwareBrowser(stage=stage)
    confirm = software_browser.show_menu(position=[0.5, 0.25])
    if not confirm:
        return
    elif software_browser.software is None:
        return

    software = software_browser.software

    comment_box = CommentEditMenu(title="Comment: ", default_comment="New file")
    confirm = comment_box.show_menu(position=[0.5, 0.3])
    if not confirm:
        return

    # reserve version
    if stage.work_component is None:
        stage.create_work_component(extension=software.extension)
        stage.reload()
    version = stage.work_component.create_last_version(software=software)
    version.update(comment=comment_box.comment)

    # create file
    file = version.to_file()
    file.new_file()
    print(f"Created file: {file.filepath}")


# TODO: Version.increment()
def increment(old_version: Version):
    comment_box = CommentEditMenu(title="Comment: ", default_comment=f"Increment from v{old_version.number:03d}")
    confirm = comment_box.show_menu(position=[0.5, 0.3])

    if not confirm:
        return

    # reserve version
    new_version = old_version.component.create_last_version(software=old_version.software)
    new_version.update(comment=comment_box.comment)

    # create file
    file = old_version.to_file()
    file.save_as(filepath=new_version.filepath)
