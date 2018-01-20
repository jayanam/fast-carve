import bpy

# TODO: Implement immediate mode
class FC_Immediate_Mode_Operator(bpy.types.Operator):
    bl_idname = "scene.fc_immediate_mode_op"
    bl_label = "Immediate Mode Operator"
    bl_description = ""
    bl_options = {"REGISTER"}

    def invoke(self, context, event):
        args = (self, context)
    
        context.area.tag_redraw()
        
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        return {'CANCELLED'}

    def finish(self):
        return {"FINISHED"}

    