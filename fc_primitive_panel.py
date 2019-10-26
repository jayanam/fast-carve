import bpy
from bpy.types import Panel

class FC_PT_Primitive_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Primitives"
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
        col = row.column()
        col.prop(context.scene, "extrude_mesh", text="Extrude")
        
        col = row.column()
        col.prop(context.scene, "fill_mesh", text="Fill")

        row = layout.row()
        col = row.column()
        col.prop(context.scene, "use_snapping", text="Snap grid")

        col = row.column()
        col.prop(context.scene, "snap_to_target", text="Snap target")

        row = layout.row()

        row.operator("object.fc_immediate_mode_op", text="Primitive Mode")
