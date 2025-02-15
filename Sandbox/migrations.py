from Cython.Shadow import returns

from MangoEngine.document_models import Stage
from MangoEngine import mongo_dialog


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


if __name__ == '__main__':
    return