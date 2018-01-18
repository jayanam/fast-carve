import bpy
from bpy.types import Panel

class FC_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "Booleans"
    bl_context = "objectmode"
    bl_category = "Fast Carve"
    
    def draw(self, context):
        global custom_icons;
        
        layout = self.layout
        scene = context.scene
        
        # Carver Target
        row = layout.row()
        layout.prop_search(context.scene, "carver_target", context.scene, "objects", text="Target Object")
            
        # New row
        row = layout.row()

        # Bool diff button
        row = layout.row()
        row.operator('object.bool_diff', text='Difference', icon='MOD_MESHDEFORM')
        
        # Bool union button
        row = layout.row()
        row.operator('object.bool_union', text='Union', icon='MOD_MESHDEFORM')
        
        # Bool Slice button
        row = layout.row()
        row.operator('object.bool_slice', text='Slice', icon='MOD_MESHDEFORM')