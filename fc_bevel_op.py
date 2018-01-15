import bpy
from bpy.types import Operator

bpy.types.Scene.carver_target = bpy.props.StringProperty()

class FC_BevelOperator(Operator):
    bl_idname = "obj.bevel"
    bl_label = "Bevel an object"
    bl_description = "Bevels a selected object" 
    bl_options = {'REGISTER', 'UNDO'} 
            
    def execute(self, context):
        
        # We know that we are in object mode
        # cause the operator is for OM only
        bpy.ops.object.select_all(action='DESELECT')

        target_obj = bpy.data.objects[bpy.context.scene.carver_target]
        target_obj.select = True
        bpy.context.scene.objects.active = target_obj
        
        # Set smooth shading for the target object
        bpy.ops.object.shade_smooth()
        
        # Set the data to autosmooth
        bpy.context.object.data.use_auto_smooth = True
        bpy.context.object.data.auto_smooth_angle = 1.0472
        
        # Remove the bevel modifier if exists
        modifier_to_remove = target_obj.modifiers.get("Bevel")
        if(not modifier_to_remove is None):
            target_obj.modifiers.remove(modifier_to_remove)
         
        # Add a new bevel modifier
        bpy.ops.object.modifier_add(type = 'BEVEL')

        # get the last added modifier
        bevel = target_obj.modifiers[-1]
        bevel.limit_method = 'WEIGHT'
        bevel.edge_weight_method = 'LARGEST'
        bevel.use_clamp_overlap = False
        bevel.width = 0.02
        bevel.segments = 3
        bevel.profile = 0.7
        
        # switch to edit mode and select sharp edges
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.edges_select_sharp()
        
        # Mark edges as sharp
        bpy.ops.mesh.mark_sharp()
        bpy.ops.transform.edge_bevelweight(value=1)

        # Back to object mode
        bpy.ops.object.editmode_toggle()
        
        return {'FINISHED'} 