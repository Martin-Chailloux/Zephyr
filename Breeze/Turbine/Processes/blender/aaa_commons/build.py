from Turbine.Processes.aaa_commons.in_out_steps import CreateFileStep, SaveStep
from Turbine.Processes.blender.aaa_commons.common_steps import CreateCollectionStep
from Turbine.tb_core import BuildProcess


class BlenderBuildProcess(BuildProcess):
    name = "blender_commons_build"
    label = "Build"
    tooltip = "Builds a scene with an empty 'Export' collection"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_file_step = CreateFileStep(version=self.Context.version)
        self.create_export_collection_step = CreateCollectionStep(name="Work")
        self.create_work_collection_step = CreateCollectionStep(name="Export")
        self.save_step = SaveStep()

        self.add_steps([
            self.create_file_step,
            self.create_export_collection_step,
            self.create_work_collection_step,
            self.save_step,
        ])

    def _inner_run(self, **kwargs):
        self.create_file_step.run()
        self.create_export_collection_step.run()
        self.create_work_collection_step.run()
        self.save_step.run(file=self.create_file_step.file)
