from typing import Optional

from Api.project_documents import Component, Version
from Api.studio_documents import Software
from Processes.aaa_commons.in_out_steps import SaveStep, OpenStep, SaveAsStep, StepLabel
from Processes.blender.aaa_commons.common_steps import CreateCollectionStep
from Api.turbine.step import StepBase
from Api.turbine.process import ProcessBase


class GetTemplateStep(StepBase):
    # TODO:
    #  - make generic with args to find the correct template
    #  - version num
    label = "Get template scene"
    def __init__(self):
        super().__init__()
        self.version: Optional[Version] = None

    def _is_success(self) -> bool:
        return self.version is not None

    def _inner_run(self):
        template_component = Component.objects.get(longname='Templates_startup_Blender_modeling_work')
        version = template_component.get_last_version()
        self.version = version


class CreateBuiltVersionStep(StepBase):
    label = "Create version"

    def __init__(self, component: Component):
        super().__init__()
        self.component = component
        self.version: Optional[Version] = None

    def _is_success(self) -> bool:
        return self.version is not None

    def _inner_run(self):
        software = Software.objects.get(label='Blender')
        version = self.component.create_last_version(software=software)
        version.update(comment="Built file")
        self.version = version


class BlenderBuild(ProcessBase):
    name = "blender_commons_build"
    label = "Build"
    tooltip = "Builds a scene with empty collections, 'Work', 'Export', and 'Sandbox'"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_step = StepLabel(label="Init")
        self.get_template_step = GetTemplateStep()
        self.open_step = OpenStep()
        self.create_built_version_step = CreateBuiltVersionStep(component=self.Context.component)
        self.save_as_step = SaveAsStep()

        self.build_step = StepLabel(label="Build")
        self.create_work_collection_step = CreateCollectionStep(name="Work")
        self.create_export_collection_step = CreateCollectionStep(name="Export")
        self.create_sandbox_collection_step = CreateCollectionStep(name="Sandbox")
        self.save_step = SaveStep()

        self.add_steps([
            self.init_step,
            self.build_step,
        ])

        self.init_step.add_step(self.get_template_step),
        self.init_step.add_step(self.open_step),
        self.init_step.add_step(self.create_built_version_step),
        self.init_step.add_step(self.save_as_step),

        self.build_step.add_step(self.create_work_collection_step)
        self.build_step.add_step(self.create_export_collection_step)
        self.build_step.add_step(self.create_sandbox_collection_step)
        self.build_step.add_step(self.save_step)


    def _inner_run(self, **kwargs):
        # TODO: this init stuff could be a separated step
        self.get_template_step.run()
        self.open_step.run(version=self.get_template_step.version)
        self.create_built_version_step.run()
        self.save_as_step.run(file=self.open_step.file,
                              target_version=self.create_built_version_step.version)
        self.set_source_version(version=self.create_built_version_step.version)
        self.init_step.set_done()

        self.create_work_collection_step.run()
        self.create_export_collection_step.run()
        self.create_sandbox_collection_step.run()
        self.save_step.run(file=self.open_step.file)
        self.build_step.set_done()
