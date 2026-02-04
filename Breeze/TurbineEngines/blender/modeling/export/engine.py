from Api.turbine.step import EngineBase
from TurbineEngines.shared_engines.export import GuiExportBase
from TurbineEngines.blender.shared_steps.export_collections import ExportCollectionsStep, GetCollectionsToExportStep
from TurbineEngines.shared_steps.io_steps import OpenStep

class BlenderModelingExportEngine(EngineBase):
    name = "blender_modeling_export"
    label = "Export"
    tooltip = "from a stage 'Modeling', exports the collection 'Export'"

    def _set_gui(self):
        self.gui = GuiExportBase(context=self.context)

    def _add_steps(self):
        self.open_step = self.add_step(OpenStep())
        self.scan_step = self.add_step(GetCollectionsToExportStep())
        # TODO: reserve all the versions that will be exported, to raise dont_overwrite errors earlier
        self.export_step = self.add_step(ExportCollectionsStep())

    def _inner_run(self, **kwargs):
        self.open_step.run(version=self.context.version)
        self.scan_step.run()
        self.export_step.run(collections=self.scan_step.collections)
