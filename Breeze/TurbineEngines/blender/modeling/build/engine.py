from Breeze.Api import data
from Breeze.TurbineEngines.shared_engines.build import EngineBuildBase
from Breeze.TurbineEngines.shared_steps.collect_steps import GetTemplateSceneStep
from Breeze.TurbineEngines.shared_steps.io_steps import OpenStep, SaveAsStep
from Software.Blender.blender_session import BlenderSession


class BlenderModelingBuildEngine(EngineBuildBase):
    name = "blender_modeling_build"
    label = "Build"
    tooltip = "Builds a scene for modeling"

    def _add_steps(self):
        self.get_template_step = self.add_step(step=GetTemplateSceneStep(
            category=data.Categories.templates,
            name=data.Softwares.blender,
            variant=data.Templates.build,
            stage_template=data.StageTemplates.modeling,
        ))
        self.open_step = self.add_step(OpenStep())
        self.save_as_step = self.add_step(SaveAsStep())

    def _inner_run(self):
        self.get_template_step.run()
        with BlenderSession(filepath=self.get_template_step.version.filepath) as bl:
            self.open_step.run(session=bl, version=self.get_template_step.version)
            self.save_as_step.run(session=bl, target_version=self.context.version)


