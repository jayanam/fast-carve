bl_info = {
    "name": "Fast Carve",
    "description": "Hardsurface utility Blender addon for quick and easy boolean and bevel operations",
    "author": "Jayanam",
    "version": (0, 2, 1, 0),
    "blender": (2, 79, 0),
    "location": "View3D",
    "category": "Object"}

# Blender imports
import bpy

from bpy.props import *

from . fc_bevel_op    import FC_BevelOperator
from . fc_panel       import FC_Panel
from . fc_bevel_panel import FC_Bevel_Panel
from . fc_bool_op     import FC_BoolOperator_Diff
from . fc_bool_op     import FC_BoolOperator_Union
from . fc_bool_op     import FC_BoolOperator_Slice

bpy.types.Scene.carver_target = PointerProperty(type=bpy.types.Object)

def register():
   bpy.utils.register_class(FC_Panel)
   bpy.utils.register_class(FC_Bevel_Panel)
   bpy.utils.register_class(FC_BevelOperator)
   bpy.utils.register_class(FC_BoolOperator_Diff)
   bpy.utils.register_class(FC_BoolOperator_Union)
   bpy.utils.register_class(FC_BoolOperator_Slice)
    
def unregister():
   bpy.utils.unregister_class(FC_Panel)
   bpy.utils.unregister_class(FC_Bevel_Panel)
   bpy.utils.unregister_class(FC_BevelOperator)
   bpy.utils.unregister_class(FC_BoolOperator_Diff)
   bpy.utils.unregister_class(FC_BoolOperator_Union)
   bpy.utils.unregister_class(FC_BoolOperator_Slice)
    
if __name__ == "__main__":
    register()