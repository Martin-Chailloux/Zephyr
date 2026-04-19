import bpy
import math
import mathutils


def rotate_vertices_around_origin():
    # rotmat = mathutils.Matrix.Rotation(30, 4, 'X')
    for obj in bpy.context.selected_objects:
        pos = obj.matrix_world.to_translation()
        with bpy.context.temp_override(selected_objects=[obj]):
            bpy.ops.object.editmode_toggle()
            bpy.ops.transform.rotate(value=math.pi / 2, orient_axis='X', orient_type='LOCAL', orient_matrix_type='LOCAL',
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


def keyframe_quat_from_euler(bone, x: int, y: int, z: int, frame: int):
    x = math.radians(x)
    y = math.radians(y)
    z = math.radians(z)
    euler = mathutils.Euler((x, y, z), 'XYZ')

    bone.rotation_quaternion = euler.to_quaternion()
    bone.keyframe_insert("rotation_quaternion", frame=frame)


def gym(bone, start_frame: int, spacing: int):
    frame = start_frame
    angles = [
        (0, 0, 0), (90, 0, 0), (-90, 0, 0),
        (0, 0, 0), (0, 90, 0), (0, -90, 0),
        (0, 0, 0), (0, 0, 90), (0, 0, -90),
        (0, 0, 0),
    ]
    for angle in angles:
        keyframe_quat_from_euler(bone=bone, x=angle[0], y=angle[1], z=angle[2], frame=frame)
        frame += spacing

def gym_example():
    bone = bpy.context.active_pose_bone
    print(f"{bone = }")
    gym(bone=bone, spacing=6, start_frame=1)

def add_mesh():
    bpy.ops.mesh.primitive_monkey_add()