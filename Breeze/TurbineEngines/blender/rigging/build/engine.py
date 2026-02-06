from Api import data
from TurbineEngines.blender.rigging.build.steps import ImportGeoStep
from TurbineEngines.shared_engines.build import EngineBuildBase
from TurbineEngines.shared_steps.collect_steps import GetTemplateSceneStep
from TurbineEngines.shared_steps.io_steps import OpenStep, SaveAsStep


class BlenderRiggingBuildEngine(EngineBuildBase):
    name = "blender_rigging_build"
    label = "Build"
    tooltip = "Builds a scene for rigging"

    def _add_steps(self):
        self.get_template_step = self.add_step(step=GetTemplateSceneStep(
            category=data.Categories.templates,
            name=data.Softwares.blender,
            variant=data.Templates.build,
            stage_template=data.StageTemplates.rigging,
        ))
        self.open_step = self.add_step(OpenStep())
        self.import_geo_step = self.add_step(ImportGeoStep())
        self.save_as_step = self.add_step(SaveAsStep())

    def _inner_run(self):
        self.get_template_step.run()
        self.open_step.run(version=self.get_template_step.version)
        self.import_geo_step.run()
        self.save_as_step.run(file=self.open_step.file, target_version=self.context.version)
