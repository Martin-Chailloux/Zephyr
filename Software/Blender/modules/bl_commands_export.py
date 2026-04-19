import bpy
import bl_utils


class BlenderCommandsExport:
    def get_collections(self, component_names: list[str]) -> dict:
        msg = ""
        status = "ok"
        collections: list[str] = []

        for name in component_names:
            collection_name = f'Export {name}'
            collection = bpy.data.collections.get(collection_name, None)

            if collection is None:
                msg += f"\n{name}: Could not find the collection {collection_name}. Skipping export"
            elif bl_utils.get_collection_parent(collection=collection).name != 'Exports':
                msg += f"\n{name}: {collection_name} is not a child of the collection 'Exports'. Skipping export"
            elif bl_utils.is_collection_excluded(collection=collection):
                msg += f"\n{name}: {collection_name} is excluded. skipping export"
            else:
                msg += f"\n{name}: ok, exporting the collection '{collection_name}'"
                collections.append(collection_name)

        if not collections:
            status = f"error"
            msg += f"\nDid not find any collection to export from component names {component_names}"

        result = {
            "status": status,
            "msg": msg,
            "collections": collections,
        }
        return result

    def isolate_collection(self, name: str, new_name: str = ""):
        export_collection = bpy.data.collections.get(name)
        root_collection: bpy.types.Collection = bpy.context.scene.collection

        # Parent the export collection to the root collection
        parent = bl_utils.get_collection_parent(export_collection)
        if parent is not None:
            parent.children.unlink(export_collection)
            root_collection.children.link(export_collection)

        # Delete other collections
        for collection in root_collection.children.values():
            if collection != export_collection:
                root_collection.children.unlink(collection)

        # Rename the collection
        if new_name:
            export_collection.name = new_name

        result = {
            "status": "ok",
        }
        return result
