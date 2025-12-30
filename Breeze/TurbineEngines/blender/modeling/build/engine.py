from Api import data
from Api.turbine.engine import TurbineEngine
from TurbineEngines.blender.modeling.build.inputs import BlenderModelingBuildGui
from TurbineEngines.blender.modeling.build.steps import ReserveVersionStep
from TurbineEngines.shared_steps.collect_steps import GetTemplateSceneStep
from TurbineEngines.shared_steps.io_steps import OpenStep, SaveAsStep, SaveStep


class BlenderModelingBuildEngine(TurbineEngine):
    name = "blender_modeling_build"
    label = "Build"
    tooltip = "Builds a scene for modeling"
    Gui = BlenderModelingBuildGui

    def _add_steps(self):
        self.get_template_step = self.add_step(step=GetTemplateSceneStep(
            category=data.Categories.templates,
            name=data.Softwares.blender,
            variant=data.Templates.build,
            stage_template=data.StageTemplates.modeling,
        ))

        self.create_version_group = self.add_group(label="Create version")
        self.reserve_version_step = self.create_version_group.add_step(ReserveVersionStep(component=self.context.component))
        self.open_step = self.create_version_group.add_step(step=OpenStep())
        self.save_as_step = self.create_version_group.add_step(SaveAsStep())

        self.save_step = self.add_step(SaveStep())

    def _inner_run(self):
        # TODO: build engine to write this create version part once
        self.reserve_version_step.run()
        # set the source version for this job
        source_version = self.reserve_version_step.version
        self.job.update(source_version=source_version)
        self.context.set_version(version=source_version)

        self.get_template_step.run()
        self.open_step.run(version=self.get_template_step.version)
        self.save_as_step.run(file=self.open_step.file, target_version=source_version)
        self.create_version_group.set_success()

        self.save_step.run(file=self.open_step.file)
