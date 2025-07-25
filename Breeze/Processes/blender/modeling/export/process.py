from Api.turbine.process import ProcessBase
from Processes.aaa_commons.in_out_steps import OpenStep
from Processes.blender.modeling.export.steps import CollectStep, ExportStep
from Processes.blender.modeling.export.ui import BlenderModelingExportUi


class BlenderModelingExport(ProcessBase):
    name = "blender_modeling_export"
    label = "Export"
    tooltip = "from a stage 'Modeling', exports the collection 'Export'"
    Ui = BlenderModelingExportUi
    ui: BlenderModelingExportUi

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # TODO: separator steps to organize small sub-steps with few code
        # TODO: separate into sub-steps
        # TODO: Export the same number thant the current versions
        #  <- versions override
        # TODO: Use the process inputs

        self.logger.warning(f"{self.ui.inputs.dont_overwrite = }")

        self.open_step = OpenStep()
        self.collect_step = CollectStep()
        self.export_step = ExportStep(version=self.Context.version, dont_overwrite=self.ui.inputs.dont_overwrite)

        self.add_step(self.open_step)
        self.add_step(self.collect_step)
        self.add_step(self.export_step)

    def _inner_run(self, **kwargs):
        self.open_step.run(version=self.Context.version)
        self.collect_step.run()
        self.export_step.run()
