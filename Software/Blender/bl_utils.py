from typing import Optional

import bpy


def get_collection_parent(collection: bpy.types.Collection) -> Optional[bpy.types.Collection]:
    for parent in bpy.data.collections:
        for name, child in parent.children.items():
            if name == collection.name:
                return parent
    else:
        return None
