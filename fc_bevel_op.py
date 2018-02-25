import bpy
from bpy.types import Operator


class FC_BevelOperator(Operator):
    bl_idname = "object.bevel"
    bl_label = "Bevel an object"
    bl_description = "Bevels selected objects" 
    bl_options = {'REGISTER', 'UNDO'}
    
    def get_display(mode):
        if mode == "OBJECT":
            return "Bevel Object"
        else:
            return "Sharpen Edges"
                  
    @classmethod
    def poll(cls, context):        
        return len(context.selected_objects) > 0
         
    def execute(self, context):
        
        active_obj = bpy.context.scene.objects.active 
        
        mode = context.active_object.mode
        
        # Sharpen and bevel in object mode
        if(mode == "OBJECT"):
                        
            # We know that we are in object mode
            # cause the operator is for OM only
            for target_obj in context.selected_objects:
                
                bpy.context.scene.objects.active = target_obj
                
                # Apply the scale before beveling
                bpy.ops.object.transform_apply(scale=True)
                
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
        
        # Sharpen edges in edit mode
        else:
            
            # Mark selected edges as sharp
            bpy.ops.mesh.mark_sharp()
            bpy.ops.transform.edge_bevelweight(value=1)
        
        bpy.context.scene.objects.active  = active_obj
        return {'FINISHED'} 