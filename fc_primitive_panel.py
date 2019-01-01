import bpy
from bpy.types import Panel

class FC_Primitive_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Primitives"
    bl_context = "objectmode"
    bl_category = "Fast Carve"
   
    def draw(self, context):
        
        layout = self.layout

        row = layout.row()
        layout.prop(context.scene, "primitive_type")

        row = layout.row()
        layout.prop(context.scene, "bool_mode")
        
        row = layout.row()
        layout.prop(context.scene, "draw_distance")

        row = layout.row()
        layout.prop(context.scene, "extrude_mesh")

        row = layout.row()
        layout.prop(context.scene, "use_snapping")

        row = layout.row()

        if not context.scene.in_primitive_mode:
            row.operator("object.fc_immediate_mode_op", text="Primitive Mode")
