from typing import Optional

from Data.project_documents import Version, Component
from Turbine.Processes.aaa_commons.in_out_steps import CreateFileStep, SaveStep
from Turbine.Processes.blender.aaa_commons.common_steps import CreateCollectionStep
from Turbine.tb_core import ProcessBuild, Step
from blender_file import BlenderFile


# class GetTemplateStep(Step):
    # def __init__(self):
    #     super().__init__()
    #     self.version: Optional[Version] = None
    #
    # def _is_success(self) -> bool:
    #     return self.version is not None
    #
    # def _inner_run(self):
    #     template_component = Component.objects.get(longname='Template_stsartup_Blender_work')
    #     version = template_component.get_last_version()
    #     self.version = version


class BlenderBuild(ProcessBuild):
    name = "blender_commons_build"
    label = "Build"
    tooltip = "Builds a scene with empty collections, 'Work', 'Export', and 'Sandbox'"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.get_template_step = GetTemplateStep()
        # self.open_step = OpenStep()
        self.create_file_step = CreateFileStep(version=self.Context.version)
        self.create_export_collection_step = CreateCollectionStep(name="Work")
        self.create_work_collection_step = CreateCollectionStep(name="Export")
        self.create_work_collection_step = CreateCollectionStep(name="Sandbox")
        self.save_step = SaveStep()

        self.add_steps([
            # self.get_template_step,
            # self.open_step,
            self.create_file_step,
            self.create_export_collection_step,
            self.create_work_collection_step,
            self.save_step,
        ])

    def _inner_run(self, **kwargs):
        # self.get_template_step.run()
        # self.open_step.run(filepath=self.get_template_step.version.filepath)
        self.create_file_step.run()
        self.create_export_collection_step.run()
        self.create_work_collection_step.run()
        self.save_step.run(file=self.create_file_step.file)
