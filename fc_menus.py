import bpy
from bpy.types import Menu
from . fc_bevel_op import FC_BevelOperator
from . fc_unbevel_op import FC_UnBevelOperator

class FC_Main_Menu(Menu):
    bl_label = "Fast Carve Operations"
    bl_idname = "fc_main_menu"
    
    def draw(self, context):
        layout = self.layout

        layout.operator("object.bool_diff")
        layout.operator("object.bool_union")
        layout.operator("object.bool_slice")
        layout.operator("object.bool_intersect")
        
        layout.separator()
                
        layout.operator("object.apply_bool")
        layout.operator("object.bool_target")
        
        layout.separator()   
        
        layout.operator("object.bevel", text=FC_BevelOperator.get_display(context.object.mode))
        
        layout.operator("object.unbevel", text=FC_UnBevelOperator.get_display(context.object.mode))
        layout.operator("object.mirror")
          