import mongoengine


mongoengine.connect(host="mongodb://localhost:27017", db="Studio", alias="default")
mongoengine.connect(host="mongodb://localhost:27017", db="JourDeVent", alias="current_project")

from Data import app_dialog
from Data.studio_documents import Status, User, Palette, Project, Software

from Data.project_documents import Stage, StageTemplate, Asset, Collection, Version


def update_stages_longname():
    stages = Stage.objects()
    for stage in stages:
        longname = f"{stage.current_asset.longname}_{stage.stage_template.name}"
        print(f"{stage.__repr__()}: {longname}")

        asset = stage.current_asset
        stage_template = stage.stage_template
        stage.delete()

        Stage.create(asset=asset, stage_template=stage_template)

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

def create_palette():
    Palette.create(
            name = "dev",

            white_text = "#F9F9F9",
            black_text = "#2F2F32",

            primary = "#303030",
            secondary = "#545454",
            tertiary = "#3D3D3D",
            surface = "#262626",

            purple = "#C8B8EA",
            red = "#FFC3C4",
            orange = "#FFD486",
            yellow = "#FFF2A0",
            green = "#C5FFAF",
            blue = "#6BB6FF",
            cyan = "#A5E5D9",
    )

def create_default_users():
    users = [
        ["Martin", "Martin Chailloux", "Resources/Icons/Users/user_test2"],
        ["Kim", "Ai Kim Crespin", "Resources/Icons/Users/kim_porto"],
        ["Elise", "Elise Golfouse", "Resources/Icons/Users/elise_chibi"],
        ["Chloé", "Chloé Lab", "Resources/Icons/Users/chloé"],
        ["Hugo", "Hugo Taillez", "Resources/Icons/Users/hugo_alien"],
        ["Camille", "Camille Truding", "Resources/Icons/Users/camille_coccinelle"],
    ]
    for user in users:
        User.create(pseudo=user[0], fullname=user[1], icon_path=user[2])


def remove_field():
    StageTemplate.objects.update(unset__tooltip=True)

def reload_stage_templates_software():
    stage_templates: list[StageTemplate] = StageTemplate.objects
    for stage_template in stage_templates:
        software = stage_template.software
        software = sorted(software, key=lambda k: k.label)
        stage_template.update(software=software)

def random_list_query():
    stages: list[Stage] = Stage.objects()
    print(f"{stages = }")
    stages = [s for s in stages if s.stage_template.label == "Animation"]
    print(stages)


def create_work_collections():
    for stage in Stage.objects:
        work_collection = stage.collections[0]
        # stage.update(collections = [work_collection])
        try:
            stage.create_work_collection()
        except Exception as e:
            print(f"{e = }")


if __name__ == '__main__':
    # for collection in Collection.objects:
    #     # collection.update(versions=[])
    #     # print(f"{collection = }")
    #     collection.update(recommended_version=None)
    for version in Version.objects:
        print(f"{version = }")
        print(f"{version.software = }")
        version.delete()