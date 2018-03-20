import bpy
from bpy.types import Operator
from bpy.props import StringProperty

# Set the pivot point of the active object
# to the center and add a mirror modifier
class FC_MirrorOperator(Operator):
    bl_idname = "object.mirror"
    bl_label = "Center Origin & Mirror"
    bl_description = "Mirror selected object" 
    bl_options = {'REGISTER', 'UNDO'} 
    
    @classmethod
    def poll(cls, context):
        
        mode = context.active_object.mode       
        return len(context.selected_objects) == 1 and mode == "OBJECT"
    
    def execute(self, context):
        
        cursor_location = bpy.context.space_data.cursor_location.copy()
                
        bpy.context.scene.cursor_location = (0.0, 0.0, 0.0)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        bpy.ops.object.modifier_add(type='MIRROR')    
        
        bpy.context.scene.cursor_location = cursor_location

        return {'FINISHED'}

# Symmetrize  
class FC_SymmetrizeOperator(Operator):
    bl_idname = "object.sym"
    bl_label = "Symmetrize"
    bl_description = "Symmetrize selected object" 
    bl_options = {'REGISTER', 'UNDO'}
    
    
    sym_axis = StringProperty(name="Symmetry axis", options={'HIDDEN'}, default="NEGATIVE_X")
    
        
    @classmethod
    def poll(cls, context):
        
        mode = context.active_object.mode       
        return len(context.selected_objects) == 1 and mode == "OBJECT"
    

    def execute(self, context):
        
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.symmetrize(direction=self.sym_axis)
        bpy.ops.object.mode_set(mode="OBJECT")
        
        return {'FINISHED'}