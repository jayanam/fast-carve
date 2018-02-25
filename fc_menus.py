import bpy
from bpy.types import Menu
from . fc_bevel_op import FC_BevelOperator
from . fc_unbevel_op import FC_UnBevelOperator

class FC_Main_Menu(Menu):
    bl_label = "Fast Carve Operations"
    bl_idname = "fc_main_menu"
    
    def draw(self, context):
        layout = self.layout

        layout.operator("object.bool_diff", icon="MOD_BOOLEAN")
        layout.operator("object.bool_union", icon="MOD_BOOLEAN")
        layout.operator("object.bool_slice", icon="MOD_BOOLEAN")
        layout.operator("object.bool_intersect", icon="MOD_BOOLEAN")
        
        layout.separator()
                
        layout.operator("object.apply_bool", icon="MOD_BOOLEAN")
        layout.operator("object.bool_target", icon="MOD_BOOLEAN")
        
        layout.separator()   
        
        layout.operator("object.bevel", text=FC_BevelOperator.get_display(context.object.mode), icon="MOD_BEVEL")
        
        layout.operator("object.unbevel", text=FC_UnBevelOperator.get_display(context.object.mode), icon="MOD_BEVEL")
        layout.operator("object.mirror", icon="MOD_MIRROR")
          