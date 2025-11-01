from Api import data
from Api.turbine.engine import TurbineEngine
from Api.turbine.utils import JobContext
from TurbineEngines.blender.modeling.build.inputs import BlenderModelingBuildGui
from TurbineEngines.blender.modeling.build.steps import ReserveVersionStep
from TurbineEngines.blender.shared_steps import CreateCollectionStep
from TurbineEngines.shared.collect_steps import GetTemplateSceneStep
from TurbineEngines.shared.io_steps import OpenStep, SaveAsStep, SaveStep


class BlenderModelingBuildEngine(TurbineEngine):
    name = "blender_modeling_build"
    label = "Build"
    tooltip = "Builds a scene for modeling"
    Gui = BlenderModelingBuildGui

    def __init__(self, context: JobContext):
        super().__init__(context=context)
        self.get_template_step = self.add_step(step=GetTemplateSceneStep(
            category=data.Categories.templates,
            name=data.Softwares.blender,
            variant=data.Templates.build,
            stage_template=data.StageTemplates.modeling,
        ))

        self.create_version_group = self.add_group(label="Create version")
        self.create_version_step = self.create_version_group.add_step(ReserveVersionStep(component=self.context.component))
        self.open_step = self.create_version_group.add_step(step=OpenStep())
        self.save_as_step = self.create_version_group.add_step(SaveAsStep())

        self.create_collections_group = self.add_group(label="Create collections")
        self.create_work_collection_step = self.create_collections_group.add_step(CreateCollectionStep(name="Work"))
        self.create_export_collection_step = self.create_collections_group.add_step(CreateCollectionStep(name="Export"))
        self.create_sandbox_collection_step = self.create_collections_group.add_step(CreateCollectionStep(name="Sandbox"))

        self.save_step = self.add_step(SaveStep())

    def _inner_run(self):
        self.get_template_step.run()

        # create a new version, then set the source version for this job
        self.create_version_step.run()
        source_version = self.create_version_step.version
        self.job.update(source_version=source_version)
        self.context.set_version(version=source_version)

        self.open_step.run(version=self.get_template_step.version)
        self.save_as_step.run(file=self.open_step.file, target_version=source_version)
        self.create_version_group.set_success()

        self.create_work_collection_step.run()
        self.create_export_collection_step.run()
        self.create_sandbox_collection_step.run()
        self.create_collections_group.set_success()

        self.save_step.run(file=self.open_step.file)
