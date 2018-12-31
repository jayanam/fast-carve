import bpy
from bpy.types import Operator

import bgl
import blf

import bmesh

import gpu
from gpu_extras.batch import batch_for_shader

from .utils.fc_bool_util import select_active, execute_boolean_op, execute_slice_op, is_apply_immediate
from .utils.fc_view_3d_utils import *
from .types.shape import *

# Immediate mode operator
class FC_Primitive_Mode_Operator(bpy.types.Operator):
    bl_idname = "object.fc_immediate_mode_op"
    bl_label = "Primitive Mode Operator"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO", "BLOCKING"}

    @classmethod
    def poll(cls, context): 
        return context.object.mode == "OBJECT"
		
    def __init__(self):
        self.draw_handle_2d = None
        self.draw_handle_3d = None
        self.draw_event  = None
        self.shape = Polyline_Shape()

        self.create_batch(None)
                
    def invoke(self, context, event):
        args = (self, context)  

        self.create_shape(context)                 

        self.register_handlers(args, context)
                   
        context.window_manager.modal_handler_add(self)

        return {"RUNNING_MODAL"}
    
    def register_handlers(self, args, context):
        self.draw_handle_3d = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback_3d, args, "WINDOW", "POST_VIEW")

        self.draw_handle_2d = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback_2d, args, "WINDOW", "POST_PIXEL")

        self.draw_event = context.window_manager.event_timer_add(0.1, window=context.window)
        
    def unregister_handlers(self, context):
        
        context.window_manager.event_timer_remove(self.draw_event)
        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle_2d, "WINDOW")
        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle_3d, "WINDOW")
        
        self.draw_handle_2d = None
        self.draw_handle_3d = None
        self.draw_event  = None

    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()
                               
        if event.type == "ESC" and event.value == "PRESS":

            is_none = self.shape.is_none()

            self.shape.reset()
            self.create_batch(None)

            if is_none:
                self.unregister_handlers(context)
                return {'CANCELLED'}

        # The mouse is moved
        if event.type == "MOUSEMOVE":

            # TODO: Handling for different shapes           
            # 1. Polyline
            # 2. Circle
            mouse_pos = get_mouse_3d_vertex(event, context)

            if self.shape.handle_mouse_move(mouse_pos, event, context):
                self.create_batch(mouse_pos)
        
        # Left mouse button is pressed
        if event.value == "PRESS" and event.type == "LEFTMOUSE":
            
            mouse_pos = get_mouse_3d_vertex(event, context)

            self.create_shape(context)

            if self.shape.handle_mouse_press(mouse_pos, event, context):
                self.create_object(context)
                self.shape.reset()
                
            self.create_batch(mouse_pos)

        # Return (Enter) key is pressed
        # if event.type == "RET" and event.value == "PRESS":

        #     if self.shape.handle_apply():
        #         self.create_object(context)
        #         self.shape.reset()

        #     self.create_batch(get_mouse_3d_vertex(event, context))
             
        return {"PASS_THROUGH"}

    def create_shape(self, context):
        if self.shape.is_none():
            if context.scene.primitive_type == "Circle":
                self.shape = Circle_Shape()
            else:
                self.shape = Polyline_Shape()

    def create_object(self, context):

        # Create a mesh and an object and 
        # add the object to the scene collection
        mesh = bpy.data.meshes.new("MyMesh")
        obj  = bpy.data.objects.new("MyObject", mesh)

        bpy.context.scene.collection.objects.link(obj)
        
        bpy.ops.object.select_all(action='DESELECT')

        bpy.context.view_layer.objects.active = obj
        obj.select_set(state=True)

        # Create a bmesh and add the vertices
        # added by mouse clicks
        bm = bmesh.new()
        bm.from_mesh(mesh) 

        for v in self.shape.vertices:
            bm.verts.new(v)
        
        bm.verts.index_update()

        bm.faces.new(bm.verts)

        # Extrude mesh if extrude mesh option is enabled
        self.extrude_mesh(context, bm)

        bm.to_mesh(mesh)  
        bm.free()

        bpy.context.view_layer.objects.active = obj
        obj.select_set(state=True)

        self.remove_doubles()
       
        # set origin to geometry
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

        # Fast bool modes
        if context.scene.bool_mode != "Create":

            target_obj = bpy.context.scene.carver_target
            if target_obj is not None:
                execute_boolean_op(context, target_obj, 
                self.get_bool_mode_id(context.scene.bool_mode))

                # delete the bool object if apply immediate is checked
                if is_apply_immediate():
                    bpy.ops.object.delete()
                    select_active(target_obj)

    def get_bool_mode_id(self, bool_name):
        if bool_name == "Difference":
            return 0
        elif bool_name == "Union":
            return 1

        # TODO: Add slice operation to bool modes
        elif bool_name == "Slice":
            return 2
        return -1

    def remove_doubles(self):
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles()       

    def extrude_mesh(self, context, bm):
        if context.scene.extrude_mesh:
            dir = get_view_direction(context) * 2.0 * context.scene.draw_distance
 
            r = bmesh.ops.extrude_face_region(bm, geom=bm.faces[:])
            verts = [e for e in r['geom'] if isinstance(e, bmesh.types.BMVert)]
            bmesh.ops.translate(bm, vec=dir, verts=verts)


    def finish(self):
        self.unregister_handlers(bpy.context)
        return {"FINISHED"}

    def create_batch(self, mouse_pos = None):
        
        points = self.shape.get_vertices_copy(mouse_pos)

        self.shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')         
        self.batch = batch_for_shader(self.shader, 'LINE_STRIP', 
            {"pos": points})

	# Draw handler to paint in pixels
    def draw_callback_2d(self, op, context):

        # Draw text for primitive mode
        region = context.region
        text = "- Primitive mode -"

        subtext = self.shape.get_text(context)

        xt = int(region.width / 2.0)
        
        blf.size(0, 24, 72)
        blf.position(0, xt - blf.dimensions(0, text)[0] / 2, 60 , 0)
        blf.draw(0, text) 

        blf.size(1, 16, 72)
        blf.color(1, 1, 1, 1, 1)
        blf.position(1, xt - blf.dimensions(1, subtext)[0] / 2, 30 , 1)
        blf.draw(1, subtext) 

	# Draw handler to paint onto the screen
    def draw_callback_3d(self, op, context):

        # Draw lines
        bgl.glLineWidth(5)
        self.shader.bind()
        self.shader.uniform_float("color", (0.1, 0.3, 0.7, 1.0))
        self.batch.draw(self.shader)
