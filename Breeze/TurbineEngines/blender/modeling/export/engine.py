from Api.turbine.step import TurbineEngine
from TurbineEngines.blender.modeling.export.inputs import BlenderModelingExportGui
from TurbineEngines.blender.shared_steps.export_collections import ExportCollectionsStep, GetCollectionsToExportStep

from TurbineEngines.shared_steps.io_steps import OpenStep


class BlenderModelingExportEngine(TurbineEngine[BlenderModelingExportGui]):
    name = "blender_modeling_export"
    label = "Export"
    tooltip = "from a stage 'Modeling', exports the collection 'Export'"
    Gui = BlenderModelingExportGui

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _add_steps(self):
        self.open_step = self.add_step(OpenStep())
        self.scan_step = self.add_step(GetCollectionsToExportStep())
        self.export_step = self.add_step(ExportCollectionsStep())

    def _inner_run(self, **kwargs):
        self.open_step.run(version=self.context.version)
        self.scan_step.run()
        self.export_step.run(collections=self.scan_step.collections)
