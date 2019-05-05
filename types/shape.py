from enum import Enum

import blf

from math import sin, cos, pi, radians

from mathutils import Vector, geometry

from mathutils.geometry import intersect_line_plane

from ..utils.fc_view_3d_utils import *

from bpy_extras.view3d_utils import (
    region_2d_to_location_3d, 
    location_3d_to_region_2d )

from .action import Action

class ShapeState(Enum):
    NONE = 0
    PROCESSING = 1
    CREATED = 2

class ViewRegion():
    def __init__(self, region):
        self._width = region.width
        self._height = region.height

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height


class ViewContext():

    def __init__(self, context):
        self._region_3d = context.space_data.region_3d
        self._view_rot  = self._region_3d.view_rotation.copy()
        self._view_mat  = self._region_3d.view_matrix.copy()
        self._pers_mat  = self._region_3d.perspective_matrix.copy()
        self._view_pers = self._region_3d.view_perspective
        self._is_perspective = self._region_3d.is_perspective
        self._region = ViewRegion(context.region)

    @property
    def region(self):
        return self._region

    @property
    def region_3d(self):
        return self._region_3d

    @property
    def view_rotation(self):
        return self._view_rot

    @property
    def view_perspective(self):
        return self._view_pers

    @property
    def perspective_matrix(self):
        return self._pers_mat

    @property
    def view_matrix(self):
        return self._view_mat

    @property
    def is_perspective(self):
        return self._is_perspective


class Shape:

    def __init__(self):
        self._state = ShapeState.NONE
        self._vertices_2d = []
        self._vertices = []
        self._vertices_extruded = []
        self._vertex_moving = None
        self._is_moving = False
        self._is_rotating = False
        self._is_extruding = False
        self._move_offset = 0.0
        self._rotation = 0.0
        self._extrusion = 0.0
        self._view_context = None
        self._mouse_pos_2d = (0,0)
        self._is_extruded = False
        self._snap_to_target = True
        self._bvhtree = None
        self._hit = None
        self._normal = None
        self._actions = []

    def get_3d_for_2d(self, pos_2d, context):

        result = None

        if self._bvhtree is None:
            return result

        origin, direction = get_origin_and_direction(pos_2d, context)

        if self._hit is None:
            self._hit, self._normal, *_ = self._bvhtree.ray_cast(origin, direction)
            if self._hit is not None:
                result =  self._hit.copy()
        else:
            result = intersect_line_plane(origin, origin + direction, self._hit, self._normal)
        
        if result is not None:
            result += self._normal.normalized() * 0.01

        return result


    def initialize(self, context, target, snap_to_target):
        if target != None:
            self._bvhtree = bvhtree_from_object(context, target)
            
        self._snap_to_target = snap_to_target
        self.build_actions()

    def is_none(self):
        return self._state is ShapeState.NONE
 
    def is_processing(self):
        return self._state is ShapeState.PROCESSING

    def is_created(self):
        return self._state is ShapeState.CREATED

    def is_extruded(self):
        return self._is_extruded

    def is_moving(self):
        return self._is_moving

    def is_rotating(self):
        return self._is_rotating

    def is_extruding(self):
        return self._is_extruding

    def set_vertex_moving(self, mouse_pos_3d):

        if mouse_pos_3d is None:
            self._vertex_moving = None
            return False

        min_dist = 1000
        idx = 0
        for i, v in enumerate(self._vertices):
            dist = (mouse_pos_3d - v).length
            if dist < min_dist:
                min_dist = dist
                idx = i

        if min_dist > 0.1:
            return False

        self._vertex_moving = idx
        return True


    def get_dir(self):
        if not self._snap_to_target or self._normal == None:
            view_rot = self._view_context.view_rotation
            return get_view_direction_by_rot_matrix(view_rot)

        return -self._normal

    def get_view_context(self):
        return self._view_context

    def set_view_context(self, value):
        self._view_context = value

    @property
    def vertices(self):
        return self._vertices

    @property
    def vertices_extruded(self):
        return self._vertices_extruded

    @property
    def vertices_2d(self):
        return self._vertices_2d

    @vertices.setter
    def vertices(self, value):
        self._vertices = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self.build_actions()

    def build_actions(self):
        self._actions.clear()

    def add_action(self, action, shape_state = None):
        if(self.state == shape_state or shape_state == None):
            self.actions.append(action)

    def get_prim_id(self):
        if(self.state == ShapeState.NONE):
            return "P"
        else:
            return ""

    def get_esc_title(self):
        if(self.state == ShapeState.NONE):
            return "Exit"
        else:
            return "Undo"

    @property
    def actions(self):
        return self._actions

    @property
    def extrusion(self):
        return self._extrusion

    def add_vertex(self, vertex):
        self._vertices.append(vertex)

    def reset(self):
        self._vertices.clear()     
        self._vertices_extruded.clear()   
        self._vertices_2d.clear()
        self.state = ShapeState.NONE

    def close(self):            
        return False

    def get_vertices_copy(self, mouse_pos = None):
        return self._vertices.copy()

    def get_vertices_extruded_copy(self, mouse_pos = None):
        return self._vertices_extruded.copy()

    def start_move(self, mouse_pos):
        if self.is_created() and mouse_pos is not None:
            self._is_moving = True
            self._move_offset = mouse_pos
            return True
        return False

    def stop_move(self, context):

        for index, vertex_3d in enumerate(self._vertices):
            rv3d = self._view_context.region_3d
            region = self._view_context.region
            self._vertices_2d[index] = location_3d_to_region_2d(region, rv3d, vertex_3d)

        self._is_moving = False
        self._move_offset = 0.0

    def start_rotate(self, mouse_pos, context):
        return False

    def stop_rotate(self, context):
        self._is_rotating = False
        self._rotation = 0.0

    def start_extrude(self, mouse_pos_2d, context):
        self._mouse_pos_2d = mouse_pos_2d
        self._is_extruding = True
        return True

    def can_set_center_type(self):
        return False

    def extrude_vertices(self, context):

        dir = self.get_dir() * self._extrusion

        for index, vertex3d in enumerate(self._vertices):    
            if not self._is_extruded:
                self._vertices_extruded.append(vertex3d + dir)
            else:
                self._vertices_extruded[index] = vertex3d + dir

        self._is_extruded = True

    def stop_extrude(self, context):
        self._is_extruding = False

    def handle_mouse_wheel(self, inc, context):
        return False

    def handle_mouse_move(self, mouse_pos_2d, mouse_pos_3d, event, context):

        if self.is_extruding():
            
            self._extrusion += (mouse_pos_2d[0] - self._mouse_pos_2d[0]) / 40

            self.extrude_vertices(context)

            self._mouse_pos_2d = mouse_pos_2d
            return True

        if self._vertex_moving is not None:
           self._vertices[self._vertex_moving] = mouse_pos_3d
           return True

        if self.is_created() and self._is_moving:
            diff = mouse_pos_3d - self._move_offset
            self._vertices = [vertex + diff for vertex in self._vertices]           
            self._vertices_extruded = [vertex + diff for vertex in self._vertices_extruded]  
            self._move_offset = mouse_pos_3d
            return True

        
        return False

    def handle_mouse_press(self, mouse_pos_2d, mouse_pos_3d, event, context):
        return False

    def handle_apply(self):
        if self.is_processing():
            if not self.close():
                self.reset()

        # The shape is created, apply the shape
        elif self.is_created():
            return True

        return False

    def draw_text(self):
        pass

    def get_point_size(self):
        return 10