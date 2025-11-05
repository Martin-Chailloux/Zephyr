import importlib
import traceback
from typing import Optional, Type, Self

from Api.document_models.project_documents import Version, Job
from Api.document_models.studio_documents import Process
from Api.turbine.inputs_gui import TurbineGui
from Api.turbine.step import TurbineStep
from Api.turbine.utils import JobContext


class TurbineEngine(TurbineStep):
    name: str = "process_name"
    label: str = "process_label"
    tooltip: str = "process_tooltip"
    Gui: Type[TurbineGui] = TurbineGui

    @classmethod
    def from_database(cls, process: Process, context: JobContext) -> Self:
        """ Returns the instance of TurbineEngine that matches the given process """
        module_path, class_name = process.class_path.rsplit('.', 1)
        try:
            module = importlib.import_module(module_path)
        except:
            raise ValueError(f"module not found from path {module_path}")
        ProcessEngine: Type[Self] = getattr(module, class_name)
        engine = ProcessEngine(context=context)
        return engine

    @classmethod
    def get_related_process(cls) -> Process | None:
        process = Process.objects(longname=cls.name)
        if process:
            return process[0]
        else:
            return None

    @classmethod
    def register(cls):
        """ Create the Process in the database, or update it if it exists """
        process = cls.get_related_process()
        if process is None:
            Process.create(longname=cls.name, class_path=cls.get_class_path(), label=cls.label, tooltip=cls.tooltip)
        else:
            process.update(class_path=cls.get_class_path(), label=cls.label, tooltip=cls.tooltip)

    def __init__(self, context: JobContext):
        super().__init__(sub_label=None)
        self.context = context
        self.gui = self.Gui(context=context)
        self.update_context()
        self.job: Optional[Job] = None

    def update_context(self):
        """ update the Context based on the given inputs """
        inputs = self.gui.inputs
        if inputs is None:
            return

        if inputs.use_last_version:
            version = self.context.component.get_last_version()
        elif inputs.version_number is not None:
            version = self.context.component.get_version(number=inputs.version_number)
        else:
            version = None

        self.context.set_version(version=version)

    def set_gui(self, gui: TurbineGui):
        self.gui = gui

    def _add_steps(self):
        """ Add steps here rather than during init so that inputs can be updated in-between """
        pass

    def run(self):
        self._add_steps()
        self.job = self.create_job()
        self.Pill.set_idle()

        self.logger.debug(f"{self.gui.inputs = }")
        self.Pill.set_running()

        try:
            super().run()
            self.Pill.set_success()
        except RuntimeError:
            print(f"{self.label = }")
            print(traceback.format_exc(chain=False))
            self.Pill.set_error()

        self.update_job()

    def on_sub_step_updated(self):
        super().on_sub_step_updated()
        self.update_job()
    # ------------------------
    # process
    # ------------------------

    @classmethod
    def get_class_path(cls):
        path = f"{cls.__module__}.{cls.__qualname__}"
        return str(path)

    # ------------------------
    # jobs
    # ------------------------
    def create_job(self) -> Job:
        """ Saves this engine's run as a Job in the db"""
        self.register()
        source_process = Process.objects.get(longname=self.name, label=self.label, tooltip=self.tooltip, class_path=self.get_class_path())

        job = Job.create(source_process=source_process,
                         steps=self.to_dict(),
                         inputs=self.gui.to_database(),
                         user=self.context.user,
                         version=self.context.version,
                         creation_time=self.context.creation_time)
        return job

    def update_job(self):
        """ Updates the current job """
        self.job.update(steps=self.to_dict())
