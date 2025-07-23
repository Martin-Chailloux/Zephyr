from pathlib import Path

import mongoengine


mongoengine.connect(host="mongodb://localhost:27017", db="Studio", alias="default")

from Api.studio_documents import User, Palette, Project, Process
from Api.breeze_app import BreezeApp
BreezeApp.set_project("JourDeVent")
BreezeApp.set_user("Martin")
from Api.studio_documents import StageTemplate
from Api.project_documents import Stage, Asset, Version, Job
from Processes.blender.aaa_commons.build import BlenderBuild
from Processes.blender.modeling.export.process import BlenderModelingExport

mongoengine.connect(host="mongodb://localhost:27017", db="JourDeVent", alias="current_project")


def update_stages_longname():
    stages = Stage.objects()
    for stage in stages:
        longname = f"{stage.asset.longname}_{stage.stage_template.name}"
        print(f"{stage.__repr__()}: {longname}")

        asset = stage.asset
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
        work_collection = stage.components[0]
        # stage.update(collections = [work_collection])
        try:
            stage.create_work_component()
        except Exception as e:
            print(f"{e = }")

def set_root_paths():
    p = Path.home().joinpath("OneDrive", "Documents", "__work", "_dev", "zephyr_projects")
    for project in Project.objects:
        project.update(root_path=str(p.joinpath(project.name)))

def register_processes():
    for process in Process.objects():
        process.delete()

    BlenderBuild.register_mg_process()
    BlenderModelingExport.register_mg_process()
    processes = Process.objects()
    for obj in StageTemplate.objects():
        obj.update(processes=processes)

def clear_versions():
    for version in Version.objects():
        if 'Templates' not in version.component.selected_stage.asset.category:
            version.delete()

def clear_jobs():
    for job in Job.objects():
        job.delete()

if __name__ == '__main__':
    clear_jobs()