from typing import Optional

import bpy

# TODO: put in /bl_utils/collections if it scales up a lot

def get_collection(name: str) -> bpy.types.Collection:
    collection = bpy.data.collections.get(name, None)
    if collection is None:
        raise ValueError(f"Did not find a collection with name: {name}")
    return collection


def get_collection_parent(collection: bpy.types.Collection) -> Optional[bpy.types.Collection]:
    for parent in bpy.data.collections:
        for name, child in parent.children.items():
            if name == collection.name:
                return parent
    else:
        return None


def get_layer_collections(view_layer: bpy.types.ViewLayer=None, collection: bpy.types.Collection=None, expect_one: bool=False) -> list[bpy.types.LayerCollection] | bpy.types.LayerCollection :
    """
    :param view_layer: (bpy.types.ViewLayer) if None, use the context's layer
    :param collection: (bpy.types.Collection) only return the layers that match this collection
    :param expect_one: (bool) when filtering with a single collection: return a single LayerCollection or crash
    """
    view_layer = view_layer or bpy.context.view_layer

    # ------------------------
    # get all LayerCollections for the given ViewLayer
    # ------------------------
    layer_collections = list(view_layer.layer_collection.children)

    parents = layer_collections
    while parents:
        children = []
        for parent in parents:
            children.extend(list(parent.children))
        layer_collections.extend(children)
        parents = children

    if collection is None:
        return layer_collections

    # ------------------------
    # filter with a single collection
    # ------------------------
    filtered_layer_collections = []

    for layer_collection in layer_collections:
        if layer_collection.collection == collection:
            filtered_layer_collections.append(layer_collection)

    if not expect_one:
        return filtered_layer_collections
    else:
        match len(filtered_layer_collections):
            case 1:
                return filtered_layer_collections[0]
            case 0:
                raise ValueError(
                    f"Did not find any layer collection for collection {collection} in view layer {view_layer}")
            case _:
                raise ValueError(
                    f"Found multiple layer collections for collection {collection} in view layer {view_layer}: {filtered_layer_collections}")


def is_collection_excluded(collection:bpy.types.Collection, view_layer=None):
    layer_collection = get_layer_collections(view_layer=view_layer, collection=collection, expect_one=True)
    return layer_collection.exclude