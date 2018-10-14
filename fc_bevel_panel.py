import bpy
from bpy.types import Panel

from . fc_bevel_op import FC_BevelOperator
from . fc_unbevel_op import FC_UnBevelOperator

class FC_Bevel_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
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
        row.prop(context.object, "display_type", text="Display As")
                
        # Bevel button
        row = layout.row()
        
        mode = context.object.mode         
         
        row.operator('object.bevel', text=FC_BevelOperator.get_display(context.object.mode), icon='MOD_BEVEL')
                      
        if(mode == "OBJECT"):                

            
            if self.has_bevel_modifier(context.active_object):
                row = layout.row()
                row.prop(context.object.modifiers["Bevel"], "width", text="Bevel width")
                                
        # Un-Bevel button
        row = layout.row()
        row.operator('object.unbevel', text=FC_UnBevelOperator.get_display(context.object.mode), icon='MOD_BEVEL')   
  
        # Mirror                       
        row = layout.row()
        row.operator('object.mirror', text='Center Origin & Mirror', icon='MOD_MIRROR')
        
        # symmetrize negative
        row = layout.row()
        split = row.split(factor=0.33)
        col = split.column()
        col.operator('object.sym', text="-X", icon='MOD_MESHDEFORM').sym_axis = "NEGATIVE_X"
        
        col = split.column()
        col.operator('object.sym', text="-Y", icon='MOD_MESHDEFORM').sym_axis = "NEGATIVE_Y"
        
        col = split.column()
        col.operator('object.sym', text="-Z", icon='MOD_MESHDEFORM').sym_axis = "NEGATIVE_Z"
        
        # symmetrize positive
        row = layout.row()
        split = row.split(factor=0.33)
        col = split.column()
        col.operator('object.sym', text="X", icon='MOD_MESHDEFORM').sym_axis = "POSITIVE_X"
        
        col = split.column()
        col.operator('object.sym', text="Y", icon='MOD_MESHDEFORM').sym_axis = "POSITIVE_Y"
        
        col = split.column()
        col.operator('object.sym', text="Z", icon='MOD_MESHDEFORM').sym_axis = "POSITIVE_Z"
