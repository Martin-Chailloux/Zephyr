from Breeze.Api import data
from Breeze.Api.document_models.project_documents import Version
from Breeze.Api.turbine.step import Step
from Breeze.TurbineEngines.shared_steps.io_steps import OpenStep, ReserveExportVersionStep, SaveAsStep
from Software.Blender.blender_session import BlenderSession


class GetCollectionsToExportStep(Step):
    label: str = "Scan"
    tooltip: str = "Get collections to export"

    def __init__(self):
        super().__init__()
        self.collections: list[str] = []

    def run(self, session: BlenderSession):
        super().run(session=session)

    def _inner_run(self, session: BlenderSession):
        component_names = self.engine.context.version.component.stage.stage_template.outputs
        result = session.get_collections_to_export(names=component_names)
        print(f"{result = }")

        status = result.get("status", "ok")
        if status != "ok":
            self.logger.error(status)

        collection_names = result.get("collections", "")
        self.logger.debug(f"{collection_names = }")
        self.collections = collection_names


class ExportCollectionsStep(Step):
    label: str = "Export"
    tooltip: str = "Export collections as .blend files"

    def run(self, session: BlenderSession, collection_names: list[str]):
        super().run(session=session, collection_names=collection_names)

    def _inner_run(self, session: BlenderSession, collection_names: list[str]):
        steps = []
        for collection in collection_names:
            step = self.add_step(ExportCollectionStep())
            step.set_sub_label(sub_label=collection)
            steps.append(step)

        for step, collection in zip(steps, collection_names):
            step.run(session=session, collection_name=collection)


class ExportCollectionStep(Step):
    label: str = "Export"
    tooltip: str = "Export a single collection as a .blend file"

    def run(self, session: BlenderSession, collection_name: str):
        super().run(session=session, collection_name=collection_name)

    def _inner_run(self, session: BlenderSession, collection_name: str):
        component_name = collection_name.replace("Export ", "")

        self.reserve_version_step = self.add_step(ReserveExportVersionStep(
            source_version=self.engine.context.version,
            component_name=component_name,
            extension=data.Extensions.blend,
        ))

        # add steps
        self.open_step = self.add_step(OpenStep())
        self.clean_step = self.add_step(IsolateCollectionStep())
        self.save_step = self.add_step(SaveAsStep())

        # run steps
        self.reserve_version_step.run()
        self.open_step.run(session=session, version=self.engine.context.version)
        self.clean_step.run(session=session, collection_name=collection_name, target_version=self.reserve_version_step.version)
        self.save_step.run(session=session, target_version=self.reserve_version_step.version)


class IsolateCollectionStep(Step):
    label: str = "Clean"
    tooltip: str = "Isolates the collection 'Export' and rename with {component asset stage}. Example: geo character_baby_-_modeling"

    def __init__(self):
        super().__init__()
        self.export_collection = None

    def run(self, session: BlenderSession, collection_name: str, target_version: Version):
        super().run(session=session, collection_name=collection_name, target_version=target_version)

    def _inner_run(self, session: BlenderSession, collection_name: str, target_version: Version):
        new_name = f"{target_version.component.name} {target_version.component.stage.longname}"
        self.logger.debug(f"{new_name = }")
        session.isolate_collection(name=collection_name, new_name=new_name)
