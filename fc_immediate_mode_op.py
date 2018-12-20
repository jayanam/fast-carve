import bpy
from bpy.types import Operator

from bpy_extras.view3d_utils import region_2d_to_origin_3d
from bpy_extras.view3d_utils import region_2d_to_location_3d

import bgl
import blf

import bmesh

import gpu
from gpu_extras.batch import batch_for_shader

import mathutils
import math

from . fc_bool_util import execute_boolean_op, execute_slice_op

       
# Immediate mode operator
class FC_Primitive_Mode_Operator(bpy.types.Operator):
    bl_idname = "object.fc_immediate_mode_op"
    bl_label = "Immediate Mode Operator"
    bl_description = ""
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context): 
        return context.active_object.mode  == "OBJECT"
		
    def __init__(self):
        self.draw_handle_2d = None
        self.draw_handle_3d = None
        self.draw_event  = None
        self.mouse_vert = None

        self.vertices = []
        self.create_batch()
                
    def invoke(self, context, event):
        args = (self, context)                   
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

    def get_snap_vertex_indizes(self, view_rot):

        v1 = round(abs(view_rot[0]), 3)
        v2 = round(abs(view_rot[1]), 3)

        # TODO: Add top / bottom snapping
        if v1== 0.5 and v2 == 0.5:
            return (1,2)
        if (v1 == 0.707 and v2== 0.707) or (v1 == 0.0 and v2 == 0.0):
           return (0,2)
        return None


    def get_mouse_3d_vertex(self, event, context):
        x, y      = event.mouse_region_x, event.mouse_region_y
        region    = context.region
        rv3d      = context.space_data.region_3d
        view_rot  = rv3d.view_rotation
        overlay3d = context.space_data.overlay
        
        dir = view_rot @ mathutils.Vector((0,0,-1))
        
        # magix number 2.0 => property?
        dir = dir.normalized() * -2.0
                   
        vec = region_2d_to_location_3d(region, rv3d, (x, y), dir)

        # we are in ortho mode, so we dont snap
        # TODO: Perhaps we also want to snap in perspective mode?
        #       Could be user-defined
        if not rv3d.is_perspective:
             
            # Now check how to snap the cursor
            ind = self.get_snap_vertex_indizes(view_rot)
            if ind is not None:               
                vec[ind[0]] = vec[ind[0]] + self.get_snap(vec[ind[0]], overlay3d)
                vec[ind[1]] = vec[ind[1]] + self.get_snap(vec[ind[1]], overlay3d)

        return vec

    
    def get_snap(self, p, overlay3d):
        ratio = overlay3d.grid_scale / overlay3d.grid_subdivisions
        ratio_half = ratio / 2.0
        mod = p % ratio
        if mod < ratio_half:
            mod = -mod
        else:
            mod = (ratio - mod)

        return mod  


    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()
                               
        if event.type in {"ESC"}:
            self.unregister_handlers(context)
            return {'CANCELLED'}
 
        if event.type == "MOUSEMOVE":
            
            # At least one vertex has been added
            if len(self.vertices) > 0:
                self.mouse_vert = self.get_mouse_3d_vertex(event, context)
                self.create_batch()
        
        if event.value == "PRESS":
            
            # Left mouse button pressed            
            if event.type == "LEFTMOUSE":
                vertex = self.get_mouse_3d_vertex(event, context)
                
                self.vertices.append(vertex)

                self.create_batch()

            # Return (Enter) key is pressed
            if event.type == "RET":
                self.create_object()
                self.unregister_handlers(context)
                return {'CANCELLED'}
                    
        return {"PASS_THROUGH"}

    def create_object(self):

        # Create a mesh and an object and 
        # add the object to the scene collection
        mesh = bpy.data.meshes.new("MyMesh")
        obj  = bpy.data.objects.new("MyObject", mesh)

        bpy.context.scene.collection.objects.link(obj)
        
        bpy.ops.object.select_all(action='DESELECT')

        bpy.context.view_layer.objects.active = obj
        obj.select_set(state=True)

        # Create a bmesh and add the vertices
        # added with mouse clicks
        bm = bmesh.new()
        bm.from_mesh(mesh) 

        for v in self.vertices:
            bm.verts.new(v)

        bm.verts.new(self.vertices[0])
        
        bm.verts.index_update()

        bm.to_mesh(mesh)  
        bm.free()

        bpy.context.view_layer.objects.active = obj
        obj.select_set(state=True)

        # fill with faces
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')

        bpy.ops.mesh.edge_face_add()
        bpy.ops.mesh.remove_doubles()
        
        # set origin to geometry
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

    def finish(self):
        self.unregister_handlers(context)
        return {"FINISHED"}

    def create_batch(self):
        
        points = self.vertices.copy()
        
        if self.mouse_vert is not None:
            points.append(self.mouse_vert)
           
        self.shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.batch = batch_for_shader(self.shader, 'LINE_STRIP', 
        {"pos": points})

	# Draw handler to paint in pixels
    def draw_callback_2d(self, op, context):
        # Draw text to indicate that draw mode is active
        region = context.region
        text = "- Primitive mode active -"
        subtext = "Esc : Close | Enter : Create"

        xt = int(region.width / 2.0)
        
        blf.size(0, 24, 72)
        blf.position(0, xt - blf.dimensions(0, text)[0] / 2, 60 , 0)
        blf.draw(0, text) 

        blf.size(1, 20, 72)
        blf.position(1, xt - blf.dimensions(0, subtext)[0] / 2, 30 , 1)
        blf.draw(1, subtext) 

	# Draw handler to paint onto the screen
    def draw_callback_3d(self, op, context):

        # Draw lines
        bgl.glLineWidth(5)
        self.shader.bind()
        self.shader.uniform_float("color", (0.1, 0.3, 0.7, 1.0))
        self.batch.draw(self.shader)

