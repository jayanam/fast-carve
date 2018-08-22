import bpy
from bpy.types import Operator


class FC_ApplyBoolOperator(Operator):
    bl_idname = "object.apply_bool"
    bl_label = "Apply Boolean"
    bl_description = "Apply pending bool operators" 
    bl_options = {'REGISTER', 'UNDO'} 
       
    @classmethod
    def poll(cls, context):        
        return len(context.selected_objects) > 0
         
    def execute(self, context):
        
        active_obj = context.active_object
              
        for obj in context.scene.objects:
            for modifier in obj.modifiers:
                if modifier.name.startswith("FC_BOOL"):
                    # API change 2.8: bpy.context.scene.objects.active = obj
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.modifier_apply(modifier=modifier.name)
        
        bpy.context.view_layer.objects.active = active_obj
        return {'FINISHED'}