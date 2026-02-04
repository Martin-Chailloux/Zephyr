import bpy

from Api import data
from Api.document_models.project_documents import Version
from Api.turbine.step import Step
import bl_utils
from TurbineEngines.shared_steps.io_steps import OpenStep, ReserveExportVersionStep, SaveAsStep


class GetCollectionsToExportStep(Step):
    label: str = "Scan"
    tooltip: str = "Get collections to export"

    def __init__(self):
        super().__init__()
        self.collections: list[bpy.types.Collection] = []

    def _inner_run(self):
        component_names = self.engine.context.version.component.stage.stage_template.outputs
        collection_names = []  # debug only
        for name in component_names:
            # get collection
            collection_name = f'Export {name}'
            collection_names.append(collection_name)
            collection = bpy.data.collections.get(collection_name, None)

            msg = None
            if collection is None:
                msg = f"Could not find the collection {collection_name}. Component '{name}' will not be exported"
                self.logger.warning(msg)
            elif bl_utils.get_collection_parent(collection=collection).name != 'Exports':
                msg = f"{collection_name} is not a child of the collection 'Exports'. Component '{name}' will not be exported"
            elif bl_utils.is_collection_excluded(collection=collection):
                msg = f"{collection_name} is excluded. Component '{name}' will not be exported"

            if msg is not None:
                self.logger.warning(msg)
            else:
                self.collections.append(collection)

        if not self.collections:
            raise ValueError(f"Did not find any collection to export. Expected: {collection_names}")
        else:
            self.logger.info(f"Found {len(self.collections)} collection(s) to export: {[c.name for c in self.collections]}")


class ExportCollectionsStep(Step):
    label: str = "Export"
    tooltip: str = "Export collections as .blend files"

    def run(self, collections: list[bpy.types.Collection]):
        super().run(collections=collections)

    def _inner_run(self, collections: list[bpy.types.Collection]):
        steps = []
        for collection in collections:
            step = self.add_step(ExportCollectionStep())
            step.set_sub_label(sub_label=collection.name)
            steps.append(step)

        for step, collection in zip(steps, collections):
            step.run(collection_name=collection.name)


class ExportCollectionStep(Step):
    label: str = "Export"
    tooltip: str = "Export a single collection as a .blend file"

    def run(self, collection_name: bpy.types.Collection):
        super().run(collection_name=collection_name)

    def _inner_run(self, collection_name: str):
        collection = bpy.data.collections.get(collection_name)
        self.logger.debug(f"{collection = }")
        component_name = collection.name.replace("Export ", "")

        self.reserve_version_step = self.add_step(ReserveExportVersionStep(
            source_version=self.engine.context.version,
            component_name=component_name,
            extension=data.Extensions.blend,
        ))

        # add steps
        self.open_step = self.add_step(OpenStep())
        self.clean_step = self.add_step(CleanExportedSceneStep())
        self.save_step = self.add_step(SaveAsStep())

        # run steps
        self.reserve_version_step.run()
        self.open_step.run(version=self.engine.context.version)
        self.clean_step.run(export_collection_name=collection_name, target_version=self.reserve_version_step.version)
        self.save_step.run(file=self.open_step.file, target_version=self.reserve_version_step.version)


class CleanExportedSceneStep(Step):
    label: str = "Clean"
    tooltip: str = "Isolates the collection 'Export' and rename with {component asset stage}. Example: geo character_baby_-_modeling"

    def __init__(self):
        super().__init__()
        self.export_collection = None

    def run(self, export_collection_name: str, target_version: Version):
        super().run(export_collection_name=export_collection_name, target_version=target_version)

    def _inner_run(self, export_collection_name: str, target_version: Version):
        export_collection = bpy.data.collections.get(export_collection_name)
        self.logger.debug(f"{export_collection = }")

        root_collection: bpy.types.Collection = bpy.context.scene.collection

        self.logger.info("Parenting the export collection to the root collection ... ")
        parent = bl_utils.get_collection_parent(export_collection)
        if parent is not None:
            parent.children.unlink(export_collection)
            root_collection.children.link(export_collection)

        self.logger.info("Deleting other collections ... ")
        for collection in root_collection.children.values():
            if collection != export_collection:
                root_collection.children.unlink(collection)

        name = f"{target_version.component.name} {target_version.component.stage.longname}"
        self.logger.info(f"Renaming the export collection to: '{name}'")
        export_collection.name = name
