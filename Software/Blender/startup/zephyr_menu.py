import bpy

import bl_commands
import bl_dialog


class BreezeTest(bpy.types.Operator):
    """ Demo operator, use to test stuff in the menu"""

    bl_idname = "breeze.test"
    bl_label = "Testing"
    bl_description = "To test stuff"

    def execute(self, context):
        print("TEST")
        return {'FINISHED'}


class BreezeSaveInc(bpy.types.Operator):
    """ Demo operator, use to test stuff in the menu"""

    bl_idname = "breeze.save_inc"
    bl_label = "Save inc"
    bl_description = "Save a new version of this file in the same location"

    def execute(self, context):
        print(f"Save inc ...")
        bl_commands.save_inc(source_filepath="test/filepath")
        # TODO: receive answer
        return {'FINISHED'}


class BreezeSaveAs(bpy.types.Operator):
    """ Demo operator, use to test stuff in the menu"""

    bl_idname = "breeze.save_as"
    bl_label = "Save as"
    bl_description = "Save a new version of this file in another location"

    def execute(self, context):
        print(f"Not implemented: Save as")
        return {'CANCELLED'}


class ZephyrMenu(bpy.types.Menu):
    bl_label = "Zephyr"
    bl_idname = "TOPBAR_MT_zephyr"

    def draw(self, context):
        layout = self.layout
        layout.operator("breeze.test")
        layout.operator("breeze.save_inc")
        layout.operator("breeze.save_as")
        layout.operator("wm.open_mainfile")
        layout.operator("wm.save_as_mainfile").copy = True

    def draw_menu(self, context):
        self.layout.menu(ZephyrMenu.bl_idname)


classes = [
    ZephyrMenu,
    BreezeTest,
    BreezeSaveInc,
    BreezeSaveAs,
]


def create():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_editor_menus.append(ZephyrMenu.draw_menu)


def remove():
    # currently not working
    # but has not been needed yet
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.TOPBAR_MT_editor_menus.remove(ZephyrMenu.draw_menu)


if __name__ == '__main__':
    create()

