import bpy
from bpy.types import Panel

# TODO: Draw some nice icons
# from . fc_icons  import get_icon

icon_collection = {}

class FC_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "Fast Carve"
    bl_context = "objectmode"
    bl_category = "jayanam"
    
    def draw(self, context):
        global custom_icons;
        
        layout = self.layout
        scene = context.scene
        
        # Carver Target
        row = layout.row()
        layout.prop_search(context.scene, "carver_target", context.scene, "objects", text="Target Object")
            
        # Bevel button
        row = layout.row()
                
        row.operator('obj.bevel', text="Sharp & Bevel", icon='MOD_MESHDEFORM')

        # Bool diff button
        row = layout.row()
        row.operator('obj.bool_diff', text='Difference', icon='MOD_MESHDEFORM')
        
        # Bool union button
        row = layout.row()
        row.operator('obj.bool_union', text='Union', icon='MOD_MESHDEFORM')