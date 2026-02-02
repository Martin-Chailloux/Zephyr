from Api.document_models.project_documents import Version
from Api.turbine.engine_gui import EngineGuiBuild
from Api.turbine.step import TurbineEngine, TurbineStep


class BuildEngineBase(TurbineEngine):
    name = "build_base"
    label = "Build"
    tooltip = "Base engine to build scenes"

    # TODO: when a build fails, show it clearly in the ui
    #  changing the display of file-less versions might do the trick
    #  (and any invalid version)

    def _set_gui(self):
        self.gui = EngineGuiBuild(context=self.context)


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


class ReserveBuiltVersionStep(TurbineStep):
    label: str = "Reserve version"
    tooltip: str = ""

    def __init__(self, number: int = -1):
        super().__init__()
        self._number = number
        self.version: Version

    def _inner_run(self):
        if self._number == -1:
            built_version = self.engine.context.component.create_last_version()
            self.logger.info(f"Created a new version... {built_version}")
        else:
            built_version = self.engine.context.component.get_version(number=self._number, crash_if_not_found=True)
            self.logger.warning(f"Building over an existing version... {built_version}")
            if self.engine.gui.get_inputs().dont_overwrite:
                raise FileExistsError(f"{built_version} already exists. Uncheck 'don't overwrite' to overwrite it.'")

        built_version.set_comment(text='Build')
        self.version = built_version
