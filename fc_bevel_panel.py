import bpy
from bpy.types import Panel

class FC_Bevel_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "Selected objects"
    bl_category = "Fast Carve"
    
    def draw(self, context):
        
        layout = self.layout
        scene = context.scene
   
        # Draw type
        row = layout.row()
        row.prop(context.object, "draw_type", text="Drawtype")
        
        # Bevel button
        row = layout.row()
        
        mode = context.active_object.mode         
           
        if(mode == "OBJECT"):                
            row.operator('object.bevel', text="Sharp & Bevel", icon='MOD_MESHDEFORM')
        else:
            row.operator('object.bevel', text="Sharpen edges", icon='MOD_MESHDEFORM')
        
        # Un-Bevel button
        row = layout.row()
                     
        if(mode == "OBJECT"):
            row.operator('object.unbevel', text="Clear Sharp & Bevel", icon='MOD_MESHDEFORM')
        else:
            row.operator('object.unbevel', text="Clear sharp edges", icon='MOD_MESHDEFORM')
            
        row = layout.row()
        row.operator('object.mirror', text='Center Origin & Mirror', icon='MOD_MESHDEFORM')