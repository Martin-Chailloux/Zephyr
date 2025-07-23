import traceback
from datetime import datetime

from Api.project_documents import Component, Version, JobContext, Job
from Api.studio_documents import User, Process
from Api.turbine.inputs_ui import ProcessInputsUi
from Api.turbine.step import StepBase


class ProcessBase(StepBase):
    name: str = "process_name"
    label = "process_label"
    tooltip = "process_tooltip"
    Ui: ProcessInputsUi = None
    ui: ProcessInputsUi  # this typing should be overridden in subclasses with the process' inputs_ui class

    def __init__(self, context: JobContext, ui: ProcessInputsUi = None):
        # NOTE: component and version are split, because a build process may use a component with 0 versions in it
        super().__init__()
        self.Context = context
        # self.Context.creation_time = datetime.now()
        self.ui = ui
        self.mg_job = self.register_mg_job()
        self.Pill.set_idle()
        print(f"{self.Context.creation_time = }")

    def run(self):
        self.Pill.set_running()

        try:
            super().run()
            self.Pill.set_success()
        except RuntimeError:
            print(f"{self.label = }")
            print(traceback.format_exc(chain=False))
            self.Pill.set_error()

        self.update_mg_job()

    def on_sub_step_updated(self):
        super().on_sub_step_updated()
        self.update_mg_job()

    def set_source_version(self, version: Version = None):
        self.mg_job.update(source_version = version)
        self.Context.set_version(version=version)

    # ------------------------
    # process
    # ------------------------
    @classmethod
    def get_class_path(cls):
        path = f"{cls.__module__}.{cls.__qualname__}"
        return str(path)

    @classmethod
    def register_mg_process(cls):
        """ Saves the process class into the db """
        # check for duplicates
        process = Process.objects(longname=cls.name)
        if process:
            process = process[0]
            process.update(label=cls.label, tooltip=cls.tooltip, class_path=cls.get_class_path())

        # create in db
        Process.create(longname=cls.name, label=cls.label, tooltip=cls.tooltip, class_path=cls.get_class_path())

    def get_registered_mg_process(self) -> Process:
        process = Process.objects.get(longname=self.name, label=self.label, tooltip=self.tooltip, class_path=self.get_class_path())
        return process

    # ------------------------
    # jobs
    # ------------------------
    def register_mg_job(self) -> Job:
        """ Saves this instantiated process as a Job in the db"""
        process = Job.create(source_process=self.get_registered_mg_process(),
                             context=self.Context,
                             steps=self.to_dict(),
                             inputs=self.ui.to_dict())
        return process

    def update_mg_job(self):
        """ Updates this instantiated process in the db"""
        self.mg_job.update(steps=self.to_dict())
