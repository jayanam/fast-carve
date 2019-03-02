import bpy
from bpy.types import Panel

class FC_Utils_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Utils"
    bl_context = "objectmode"
    bl_category = "Fast Carve"
    
    def draw(self, context):
        global custom_icons
        
        layout = self.layout
        scene = context.scene
            
        # Mirror
        row = layout.row()
        row.operator('object.mirror', text='Center Origin & Mirror', icon='MOD_MESHDEFORM')
