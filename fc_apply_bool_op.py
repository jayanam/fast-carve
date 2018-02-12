import bpy
from bpy.types import Operator


class FC_ApplyBoolOperator(Operator):
    bl_idname = "object.apply_bool"
    bl_label = "Apply bool operators"
    bl_description = "Apply pending bool operators" 
    bl_options = {'REGISTER', 'UNDO'} 
       
    @classmethod
    def poll(cls, context):        
        return len(context.selected_objects) > 0
         
    def execute(self, context):
        
        active_obj = bpy.context.scene.objects.active
              
        for obj in context.scene.objects:
            for modifier in obj.modifiers:
                if modifier.name.startswith("FC_BOOL"):
                    bpy.context.scene.objects.active = obj
                    bpy.ops.object.modifier_apply(modifier=modifier.name)
        
        bpy.context.scene.objects.active = active_obj
        return {'FINISHED'}