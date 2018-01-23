import bpy
from bpy.types import Panel

class FC_Bevel_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "Bevels"
    bl_context = "objectmode"
    bl_category = "Fast Carve"
    
    def draw(self, context):
        
        layout = self.layout
        scene = context.scene
   
        # Bevel button
        row = layout.row()
                    
        row.operator('object.bevel', text="Sharp & Bevel", icon='MOD_MESHDEFORM')
        
        # Un-Bevel button
        row = layout.row()
                    
        row.operator('object.unbevel', text="Clear Sharp & Bevel", icon='MOD_MESHDEFORM')