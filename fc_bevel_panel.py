import bpy
from bpy.types import Panel

from . fc_bevel_op import FC_BevelOperator
from . fc_unbevel_op import FC_UnBevelOperator

class FC_Bevel_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "Selected objects"
    bl_category = "Fast Carve"
    
    def has_bevel_modifier(self, obj):
        for modifier in obj.modifiers:
            if modifier.type == "BEVEL":
                return True
        return False
    
    def draw(self, context):
        
        layout = self.layout
        scene = context.scene
   
        # Draw type
        row = layout.row()
        row.prop(context.object, "draw_type", text="Drawtype")
                
        # Bevel button
        row = layout.row()
        
        mode = context.object.mode         
         
        row.operator('object.bevel', text=FC_BevelOperator.get_display(context.object.mode), icon='MOD_MESHDEFORM')
                      
        if(mode == "OBJECT"):                

            
            if self.has_bevel_modifier(context.active_object):
                row = layout.row()
                row.prop(context.object.modifiers["Bevel"], "width", text="Bevel width")
                                
        # Un-Bevel button
        row = layout.row()
        row.operator('object.unbevel', text=FC_UnBevelOperator.get_display(context.object.mode), icon='MOD_MESHDEFORM')   
                         
        row = layout.row()
        row.operator('object.mirror', text='Center Origin & Mirror', icon='MOD_MESHDEFORM')