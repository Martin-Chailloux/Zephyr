import bpy

from Api.turbine.step import StepBase


class CreateCollectionStep(StepBase):
    label = "Create collection"
    tooltip = "Creates a new empty collection under the 'Scene Collection'"

    def __init__(self, name: str):
        super().__init__(sub_label=name)
        self.collection_name = name

    def _inner_run(self):
        self.logger.info(msg=f"Creating collection: '{self.collection_name}' ... ")

        collection = bpy.data.collections.new(name=self.collection_name)
        bpy.context.scene.collection.children.link(collection)
