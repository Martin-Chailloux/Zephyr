from dataclasses import dataclass

from Api.turbine.gui import GuiBase
from Api.turbine.utils import InputsBase
from Api.turbine.gui_widgets import Specifics
from Api.turbine.step import EngineBase
from TurbineEngines.shared_steps.io_steps import ReserveBuiltVersionStep


@dataclass
class InputsBuildBase(InputsBase):
    create_new_version: bool = False


class GuiBuildBase(GuiBase):
    def _init_ui(self):
        self.allow_overwrite = self.add(Specifics.DontOverwrite())
        self.new_version = self.add(Specifics.NewVersion(context=self.context))
        self.version_number = self.add(Specifics.VersionNumber(context=self.context))
        self.version_number.combobox.setFixedWidth(64)

    def _connect_signals(self):
        self.new_version.checkbox.clicked.connect(self.on_last_version_clicked)

    def _init_state(self):
        self.on_last_version_clicked(is_checked=self.new_version.checkbox.isChecked())

    def on_last_version_clicked(self, is_checked: bool):
        self.version_number.setEnabled(not is_checked)

    def get_inputs(self) -> InputsBuildBase:
        result = InputsBuildBase(
            use_last_version=False,
            create_new_version=self.new_version.checkbox.isChecked(),
            version_number=int(self.version_number.combobox.currentText()),
            dont_overwrite=self.allow_overwrite.checkbox.isChecked(),
        )
        return result


class EngineBuildBase(EngineBase):
    name = "build_base"
    label = "Build"
    tooltip = "Base engine to build scenes"

    # TODO: when a build fails, show it clearly in the ui
    #  changing the display of file-less versions might do the trick
    #  (and any invalid version)

    def _set_gui(self):
        self.gui = GuiBuildBase(context=self.context)

    def _before_add_steps(self):
        if self.gui.get_inputs().create_new_version:
            number = -1
        else:
            number = self.gui.get_inputs().version_number
        self.reserve_version_step = self.add_step(ReserveBuiltVersionStep(
            number=number
        ))

    def _before_run(self):
        self.reserve_version_step.run()
        built_version = self.reserve_version_step.version
        self.job.update(source_version=built_version)
        self.context.set_version(version=built_version)
