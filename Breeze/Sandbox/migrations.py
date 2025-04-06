import mongoengine

from Data.studio_documents import Status

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



if __name__ == '__main__':
    # default_status = Status.objects.get(label="WAIT")
    # print(f"{default_status = }")

    for i, status in enumerate(default_statuses):
        create_status(label=status.label, color=status.color, order=i)
    # for stage in Stage.objects:
    #     print(f"{stage.status = }")
    #
    #     print(f"{stage = }")
    #     print(f"{stage.status = }")
