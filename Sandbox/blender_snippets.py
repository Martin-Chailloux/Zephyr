import bpy
from math import pi
import mathutils

def rotate_vertices_around_origin():
    # rotmat = mathutils.Matrix.Rotation(30, 4, 'X')
    for obj in bpy.context.selected_objects:
        pos = obj.matrix_world.to_translation()
        with bpy.context.temp_override(selected_objects=[obj]):
            bpy.ops.object.editmode_toggle()
            bpy.ops.transform.rotate(value=pi / 2, orient_axis='X', orient_type='LOCAL', orient_matrix_type='LOCAL',
                                     constraint_axis=(True, False, False), mirror=True, center_override=pos)

"""    
bpy.ops.view3d.snap_cursor_to_selected()
bpy.ops.object.editmode_toggle()
bpy.ops.transform.rotate(value=pi/4, orient_axis='X', orient_type='LOCAL', orient_matrix_type='LOCAL', constraint_axis=(True, False, False), mirror=True)


vertices = [v for v in object.data.vertices]
for vtx in vertices:
    # vtx.co[0] += 1
    vtx.co = vtx.co * rotmat
"""


def set_cursor_position(pos: list[float]):
    bpy.context.scene.cursor.location = pos
