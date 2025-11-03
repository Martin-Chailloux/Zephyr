from typing import Optional

import bpy

from Api.document_models.project_documents import Version
from Api.turbine.step import TurbineStep
from Api.turbine.utils import JobContext


class CreateCollectionStep(TurbineStep):
    label = "Create collection"
    tooltip = "Creates a new empty collection"

    def __init__(self, name: str):
        super().__init__(sub_label=name)
        self.collection_name = name

    def _inner_run(self):
        # TODO: error or pass if the collection exists
        self.logger.info(msg=f"Creating collection: '{self.collection_name}' ... ")

        collection = bpy.data.collections.new(name=self.collection_name)
        bpy.context.scene.collection.children.link(collection)


class GetExportCollectionStep(TurbineStep):
    label: str = "Get export collection"
    tooltip: str = ""

    def __init__(self):
        super().__init__()
        self.export_collection = None

    def _inner_run(self):
        # TODO: search for the name that matches the current export. Example: 'Export geo', and not 'Export'
        # TODO: generic method get_collection(name:str), to use here
        export_collection = bpy.data.collections.get('Export', None)
        self.logger.debug(f"{export_collection = }")
        if export_collection is None:
            raise RuntimeError("Could not find the collection 'Export'")
        self.export_collection = export_collection


class CleanExportedSceneStep(TurbineStep):
    label: str = "Clean"
    tooltip: str = "Isolates the collection 'Export' and rename with {component asset stage}. Example: geo character_baby_-_modeling"

    def __init__(self):
        super().__init__()
        self.export_collection = None

    @staticmethod  # TODO: move elsewhere
    def get_collection_parent(collection: bpy.types.Collection) -> Optional[bpy.types.Collection]:
        for parent in bpy.data.collections:
            for name, child in parent.children.items():
                if name == collection.name:
                    return parent
        else:
            return None

    def run(self, export_collection: bpy.types.Collection, target_version: Version):
        super().run(export_collection=export_collection, target_version=target_version)

    def _inner_run(self, export_collection: bpy.types.Collection, target_version: Version):
        self.logger.debug(f"{export_collection = }")

        root_collection: bpy.types.Collection = bpy.context.scene.collection

        self.logger.info("Parenting the export collection to the root collection ... ")
        parent = self.get_collection_parent(export_collection)
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
