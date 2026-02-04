import bpy

from Api.turbine.step import Step
from software_base import AbstractSoftwareFile


class ImportGeoStep(Step):
    label = "Import geo"
    tooltip = "Imports geo ingredients in the scene"

    def _inner_run(self):
        ingredients = self.engine.context.component.stage.ingredients
        geos = ingredients['geo']
        self.logger.debug(f"{geos = }")

        for version in geos:
            imported_collections: list[str] = []
            self.logger.info(f"Importing collections from {version}")
            with bpy.data.libraries.load(version.filepath) as (data_from, data_to):
                for collection_name in data_from.collections:
                    self.logger.info(f" - importing collection '{collection_name}'")
                    data_to.collections.append(collection_name)
                    imported_collections.append(collection_name)

            for collection_name in imported_collections:
                    collection = bpy.data.collections.get(collection_name)
                    bpy.context.scene.collection.children.link(collection)
