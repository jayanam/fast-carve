import bpy
from bpy.types import Menu

from . fc_bevel_op   import FC_BevelOperator as bo
from . fc_unbevel_op import FC_UnBevelOperator as ubo

class FC_Main_Menu(Menu):
    bl_idname = "OBJECT_MT_fc_main_menu"
    bl_label = "Fast Carve Operations"
    
    def draw(self, context):
        layout = self.layout

        layout.operator("object.bool_diff",  icon="MOD_BOOLEAN")
        layout.operator("object.bool_union", icon="MOD_BOOLEAN")
        layout.operator("object.bool_slice", icon="MOD_BOOLEAN")
        layout.operator("object.bool_intersect", icon="MOD_BOOLEAN")
        
        layout.separator()
                
        layout.operator("object.apply_bool",  icon="MOD_BOOLEAN")
        layout.operator("object.bool_target", icon="MOD_BOOLEAN")
        
        layout.separator()   
        
        layout.operator("object.bevel", text=bo.get_display(context.object.mode), icon="MOD_BEVEL")
        
        layout.operator("object.unbevel", text=ubo.get_display(context.object.mode), icon="MOD_BEVEL")
        layout.operator("object.mirror", icon="MOD_MIRROR")         