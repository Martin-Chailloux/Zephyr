from Breeze.Api.turbine.step import EngineBase
from Breeze.TurbineEngines.shared_engines.export import GuiExportBase
from Breeze.TurbineEngines.blender.shared_steps.export_collections import ExportCollectionsStep, GetCollectionsToExportStep
from Breeze.TurbineEngines.shared_steps.io_steps import OpenStep
from Software.Blender.blender_session import BlenderSession


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
        with BlenderSession(filepath=self.context.version.filepath) as bl:
            self.open_step.run(session=bl, version=self.context.version)
            self.scan_step.run(session=bl)
            self.logger.debug(f"{self.scan_step.collections = }")
            self.export_step.run(session=bl, collection_names=self.scan_step.collections)
