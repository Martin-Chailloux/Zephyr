from Api import data
from Api.turbine.engine import TurbineEngine
from TurbineEngines.blender.modeling.export.inputs import BlenderModelingExportGui
from TurbineEngines.shared_steps.blender_steps import GetExportCollectionStep, CleanExportedSceneStep
from TurbineEngines.shared_steps.io_steps import OpenStep, ReserveExportedVersionStep, SaveAsStep


class BlenderModelingExportEngine(TurbineEngine):
    name = "blender_modeling_export"
    label = "Export"
    tooltip = "from a stage 'Modeling', exports the collection 'Export'"
    Gui = BlenderModelingExportGui

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _add_steps(self):
        """
        - open scene
        - get collections to export
        - export each collection
        :return:
        """


        # TODO: loop over multiple exports
        self.reserve_version_step = self.add_step(ReserveExportedVersionStep(source_version=self.context.version, dont_overwrite=self.gui.inputs.dont_overwrite,
                                                                             name=data.Components.geo, label=data.Components.geo.title(), extension=data.Extensions.blend))
        self.open_step = self.add_step(OpenStep())
        self.collect_step = self.add_step(GetExportCollectionStep())

        self.export_group = self.add_group(label="Export")
        self.clean_step = self.export_group.add_step(CleanExportedSceneStep())
        self.save_as_step = self.export_group.add_step(SaveAsStep())

    def _inner_run(self, **kwargs):
        self.reserve_version_step.run()
        self.open_step.run(version=self.context.version)
        self.collect_step.run()

        self.clean_step.run(export_collection=self.collect_step.export_collection, target_version=self.reserve_version_step.version)
        self.save_as_step.run(file=self.open_step.file, target_version=self.reserve_version_step.version)
        self.export_group.set_success()
