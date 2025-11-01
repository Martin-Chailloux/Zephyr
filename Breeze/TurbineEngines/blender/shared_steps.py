import bpy

from Api.turbine.step import TurbineStep


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
