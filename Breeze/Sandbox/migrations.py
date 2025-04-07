import mongoengine

from Data.studio_documents import Status
from Dialogs.user_dialog import create_user

mongoengine.connect(host="mongodb://localhost:27017", db="Studio", alias="default")
mongoengine.connect(host="mongodb://localhost:27017", db="JourDeVent", alias="current_project")

from Data.project_documents import Stage, StageTemplate, Asset
from Data.status_model import default_statuses, StatusModel
from Dialogs import breeze_dialog
from Dialogs.status_dialog import create_status


def update_stages_longname():
    stages = Stage.objects()
    for stage in stages:
        longname = f"{stage.current_asset.longname}_{stage.stage_template.name}"
        print(f"{stage.__repr__()}: {longname}")

        asset = stage.current_asset
        stage_template = stage.stage_template
        stage.delete()

        breeze_dialog.create_stage(
            asset=asset,
            stage_template=stage_template
        )

def stage_templates_description_to_tooltip():
    stage_templates = StageTemplate.objects()
    for stage_template in stage_templates:
        old = stage_template.description
        stage_template.update(unset__description = True)
        stage_template.update(tooltip = old)


def clear_old_stages_from_assets():
    all_assets = Asset.objects
    all_stages = Stage.objects
    for asset in all_assets:
        stages = [s for s in asset.stages if s in all_stages]
        asset.update(stages=stages)


def create_default_users():
    users = [
        ["Martin", "Martin Chailloux", "Resources/Icons/Users/user_test2"],
        ["Kim", "Ai Kim Crespin", "Resources/Icons/Users/kim"],
        ["Elise", "Elise Golfouse", "Resources/Icons/Users/elise"],
        ["Chloé", "Chloé Lab", "Resources/Icons/Users/chloé"],
        ["Hugo", "Hugo Taillez", "Resources/Icons/Users/hugo"],
        ["Camille", "Camille Truding", "Resources/Icons/Users/camille"],
    ]
    for user in users:
        create_user(pseudo=user[0], fullname=user[1], icon_path=user[2])

if __name__ == '__main__':
    create_default_users()