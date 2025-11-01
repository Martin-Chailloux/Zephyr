from typing import Type

from Api.turbine.engine import TurbineEngine
from TurbineEngines.blender.modeling.export.inputs import BlenderModelingExportGui
from TurbineEngines.shared.io_steps import OpenStep
from TurbineEngines.blender.modeling.export.steps import CollectStep, ExportStep


class BlenderModelingExportEngine(TurbineEngine):
    name = "blender_modeling_export"
    label = "Export"
    tooltip = "from a stage 'Modeling', exports the collection 'Export'"
    Gui = BlenderModelingExportGui

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.open_step = self.add_step(OpenStep())
        self.collect_step = self.add_step(CollectStep())
        self.export_step = self.add_step(ExportStep(version=self.context.version, dont_overwrite=self.gui.inputs.dont_overwrite))

    def _inner_run(self, **kwargs):
        self.open_step.run(version=self.context.version)
        self.collect_step.run()
        self.export_step.run()
