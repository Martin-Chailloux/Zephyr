from Api import data
from Api.turbine.step import TurbineStep
from TurbineEngines.shared_engines.build_engine import BuildEngineBase
from TurbineEngines.shared_steps.collect_steps import GetTemplateSceneStep
from TurbineEngines.shared_steps.io_steps import OpenStep, SaveAsStep


class BlenderModelingBuildEngine(BuildEngineBase):
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
        self.open_step = self.add_step(step=OpenStep())
        self.save_as_step = self.add_step(SaveAsStep())

    def _inner_run(self):
        self.get_template_step.run()
        self.open_step.run(version=self.get_template_step.version)
        self.save_as_step.run(file=self.open_step.file, target_version=self.context.version)
