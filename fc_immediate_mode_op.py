import bpy

# Blender utils and fonts module
import blf

# Blender wrapper for opengl
import bgl

from . fc_bool_util import execute_boolean_op, execute_slice_op

def draw_bg(region):
    # Enable Opengl alpha
    bgl.glEnable(bgl.GL_BLEND)
    
    # set color: red, green, blue, alpha
    bgl.glColor4f(1.0, 0.0, 0.0, 0.1)
    
    # draw rectangle
    # x0, y0, x1, y1
    bgl.glRecti(1, 100, region.width, 0)

def create_font(id, size):
    blf.size(id, size, 72)
      
def draw_text(text, x, y, font_id):

    blf.position(font_id, x, y , 0)
    
    bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
    blf.draw(font_id, text)  
        
# Immediate mode operator
class FC_Immediate_Mode_Operator(bpy.types.Operator):
    bl_idname = "object.fc_immediate_mode_op"
    bl_label = "Immediate Mode Operator"
    bl_description = ""
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        args = (self, context)
        
        # Register draw callback
        self._handle = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback_px, args, "WINDOW", "POST_PIXEL")
        
        self._mode = 0
        
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}
    
    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type in {"ESC"}:
            return self.finish()
        
        # Change mode
        if event.type == 'M' and event.value == 'PRESS':
            self._mode = (self._mode + 1)  % 3
            return {'RUNNING_MODAL'}
        
        # Execute 
        if event.type  == 'SPACE' and event.value == 'PRESS':
            target_obj = bpy.context.scene.carver_target
            
            if self._mode < 2:
                execute_boolean_op(context, target_obj, self._mode)
            elif self._mode == 2:
                execute_slice_op(context, target_obj)
                
            return {'RUNNING_MODAL'}
        
        return {"PASS_THROUGH"}

    def finish(self):
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, "WINDOW")
        return {"FINISHED"}

        
    # Draw handler to paint onto the screen
    def draw_callback_px(tmp, self, context):
        
        region = context.region
        
        draw_bg(region)
            
        xt = int(region.width / 2.0)
                
        if self._mode == 0:
            mode = "Difference"
        elif self._mode == 1:
            mode = "Union"
        else:
            mode = "Slice"
        
        text = "Mode (M): {0}".format(mode)
        
        # Big font
        font_id = 0
        create_font(font_id, 25)
        
        # Small font 
        s_font_id = 1
        create_font(s_font_id, 10)
        
        draw_text(text, xt - blf.dimensions(font_id, text)[0] / 2, 60, font_id)
        
        text_info = "Apply: Space | Finish: Esc"
        draw_text(text_info, xt- blf.dimensions(s_font_id, text_info)[0] / 2, 30, s_font_id)
