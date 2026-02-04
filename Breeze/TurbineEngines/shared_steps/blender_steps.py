import bpy

from Api.turbine.step import Step


class CreateCollectionStep(Step):
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



class GetExportCollectionStep(Step):
    label: str = "Get export collection"
    tooltip: str = ""

    def __init__(self):
        super().__init__()
        self.export_collection = None

    def _inner_run(self):
        # TODO: search for the name that matches the current export. Example: 'Export geo', and not 'Export'
        export_collection = bpy.data.collections.get('Export', None)
        # export_collection = bpy.data.collections.get('Export - geo', None)  # hack for doc, until smarter engine
        self.logger.debug(f"{export_collection = }")
        if export_collection is None:
            raise RuntimeError("Could not find the collection 'Export'")
        self.export_collection = export_collection


