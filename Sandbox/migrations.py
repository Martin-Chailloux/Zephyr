from Cython.Shadow import returns

from Data.breeze_documents import Stage, StageTemplate, Asset

from Dialogs import breeze_dialog


def update_stages_longname():
    stages = Stage.objects()
    for stage in stages:
        longname = f"{stage.asset.longname}_{stage.stage_template.name}"
        print(f"{stage.__repr__()}: {longname}")

        asset = stage.asset
        stage_template = stage.stage_template
        stage.delete()

        mongo_dialog.create_stage(
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
    pass