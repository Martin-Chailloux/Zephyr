from Api.document_models.project_documents import Component, Version
from Api.document_models.studio_documents import Software
from Api.turbine.step import TurbineStep


class ReserveVersionStep(TurbineStep):
    label = "Reserve version"
    def __init__(self, component: Component):
        super().__init__()
        self._component = component
        self.version: Version

    def _inner_run(self):
        software = Software.objects.get(label='Blender')
        version = self._component.create_last_version(software=software)
        version.set_comment(text='Build')
        self.version = version
