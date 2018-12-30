bl_info = {
    "name": "Fast Carve",
    "description": "Hardsurface utility Blender addon for quick and easy boolean and bevel operations",
    "author": "Jayanam",
    "version": (0, 7, 7, 1),
    "blender": (2, 80, 0),
    "location": "View3D",
    "category": "Object"}

# Blender imports
import bpy

from bpy.props import *

from bpy.types import AddonPreferences

import rna_keymap_ui

from . fc_bevel_op          import FC_BevelOperator
from . fc_unbevel_op        import FC_UnBevelOperator
from . fc_panel             import FC_Panel
from . fc_bevel_panel       import FC_Bevel_Panel
from . fc_primitive_panel   import FC_Primitive_Panel
from . fc_bool_op           import FC_BoolOperator_Diff
from . fc_bool_op           import FC_BoolOperator_Union
from . fc_bool_op           import FC_BoolOperator_Slice
from . fc_bool_op           import FC_BoolOperator_Intersect
from . fc_bool_op           import FC_TargetSelectOperator
from . fc_utils_op          import FC_MirrorOperator
from . fc_utils_op          import FC_SymmetrizeOperator
from . fc_menus             import FC_Main_Menu
from . fc_apply_bool_op     import FC_ApplyBoolOperator
from . fc_immediate_mode_op import FC_Primitive_Mode_Operator

# Scene properties
bpy.types.Scene.carver_target = PointerProperty(type=bpy.types.Object)

bpy.types.Scene.apply_bool    = BoolProperty(
                                      name="Apply Immediately", 
                                      description="Apply bool operation immediately",
                                      default = True)

bpy.types.Scene.draw_distance = FloatProperty(
                                      name="Draw Distance", 
                                      description="Distance of primitives to the origin",
                                      default = 2.0)

bpy.types.Scene.extrude_mesh  = BoolProperty(name="Extrude mesh", 
                                      description="Extrude the mesh after creation",
                                      default = True)

mode_items = [ ("Create",     "Create", "", -1),
               ("Difference", "Difference", "", 0),
               ("Union",      "Union", "", 1)
             ]

bpy.types.Scene.bool_mode = bpy.props.EnumProperty(items=mode_items, 
                                                   name="Mode",
                                                   default="Create")

primitive_types = [ ("Polyline",  "Polyline", "", 0),
                    ("Circle",    "Circle",   "", 1)
                  ]

bpy.types.Scene.primitive_type = bpy.props.EnumProperty(items=primitive_types, 
                                                        name="Type",
                                                        default="Polyline")

# Addon preferences
class FC_AddonPreferences(AddonPreferences):
    bl_idname = __name__
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column()
        kc = bpy.context.window_manager.keyconfigs.addon
        for km, kmi in addon_keymaps:
            km = km.active()
            kmi.show_expanded = False
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
    

addon_keymaps = []

def register():
   bpy.utils.register_class(FC_Panel)
   bpy.utils.register_class(FC_Bevel_Panel)
   bpy.utils.register_class(FC_Primitive_Panel)
   bpy.utils.register_class(FC_BevelOperator)
   bpy.utils.register_class(FC_UnBevelOperator)
   bpy.utils.register_class(FC_BoolOperator_Diff)
   bpy.utils.register_class(FC_BoolOperator_Union)
   bpy.utils.register_class(FC_BoolOperator_Slice)
   bpy.utils.register_class(FC_BoolOperator_Intersect)
   bpy.utils.register_class(FC_TargetSelectOperator)
   bpy.utils.register_class(FC_MirrorOperator)
   bpy.utils.register_class(FC_SymmetrizeOperator)
   bpy.utils.register_class(FC_ApplyBoolOperator)
   bpy.utils.register_class(FC_Primitive_Mode_Operator)
   bpy.utils.register_class(FC_Main_Menu)
   bpy.utils.register_class(FC_AddonPreferences)
   
   # add keymap entry
   kcfg = bpy.context.window_manager.keyconfigs.addon
   if kcfg:
       km = kcfg.keymaps.new(name='3D View', space_type='VIEW_3D')
       
       kmi = km.keymap_items.new("object.fc_immediate_mode_op", 'P', 'PRESS', shift=True, ctrl=True)
       
       kmi_mnu = km.keymap_items.new("wm.call_menu", "Q", "PRESS", shift=True)
       kmi_mnu.properties.name = FC_Main_Menu.bl_idname
       kmi_mnu.active = True
       
       addon_keymaps.append((km, kmi))
       addon_keymaps.append((km, kmi_mnu))
    
def unregister():
   bpy.utils.unregister_class(FC_Panel)
   bpy.utils.unregister_class(FC_Bevel_Panel)
   bpy.utils.unregister_class(FC_Primitive_Panel)
   bpy.utils.unregister_class(FC_BevelOperator)
   bpy.utils.unregister_class(FC_UnBevelOperator)
   bpy.utils.unregister_class(FC_BoolOperator_Diff)
   bpy.utils.unregister_class(FC_BoolOperator_Union)
   bpy.utils.unregister_class(FC_BoolOperator_Slice)
   bpy.utils.unregister_class(FC_BoolOperator_Intersect)
   bpy.utils.unregister_class(FC_TargetSelectOperator)
   bpy.utils.unregister_class(FC_MirrorOperator)
   bpy.utils.unregister_class(FC_SymmetrizeOperator)
   bpy.utils.unregister_class(FC_ApplyBoolOperator)         
   bpy.utils.unregister_class(FC_Main_Menu)
   bpy.utils.unregister_class(FC_AddonPreferences)
    
   # remove keymap entry
   for km, kmi in addon_keymaps:
       km.keymap_items.remove(kmi)
   addon_keymaps.clear()
    
   bpy.utils.unregister_class(FC_Primitive_Mode_Operator)
    
if __name__ == "__main__":
    register()