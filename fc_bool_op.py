import bpy
from bpy.types import Operator

from . fc_bool_util import execute_boolean_op, execute_slice_op

class FC_BoolOperator_Diff(Operator):
    bl_idname = "object.bool_diff"
    bl_label = "Bool difference"
    bl_description = "Difference for 2 selected objects" 
    bl_options = {'REGISTER', 'UNDO'} 
            
    def execute(self, context):
        target_obj = bpy.data.objects[bpy.context.scene.carver_target]
        
        execute_boolean_op(context, target_obj, 0)
        return {'FINISHED'}
    
class FC_BoolOperator_Union(Operator):
    bl_idname = "object.bool_union"
    bl_label = "Bool union"
    bl_description = "Union for 2 selected objects" 
    bl_options = {'REGISTER', 'UNDO'} 
            
    def execute(self, context):
        target_obj = bpy.data.objects[bpy.context.scene.carver_target]
        
        execute_boolean_op(context, target_obj, 1)
        return {'FINISHED'}
    
class FC_BoolOperator_Slice(Operator):
    bl_idname = "object.bool_slice"
    bl_label = "Bool slice"
    bl_description = "Slice for 2 selected objects" 
    bl_options = {'REGISTER', 'UNDO'} 
            
    def execute(self, context):
        target_obj = bpy.data.objects[bpy.context.scene.carver_target]
        
        execute_slice_op(context, target_obj)
        return {'FINISHED'}