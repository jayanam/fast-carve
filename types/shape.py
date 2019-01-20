from enum import Enum

from math import sin, cos, pi, radians

from mathutils import Vector, geometry

from ..utils.fc_view_3d_utils import get_3d_vertex, get_view_direction_by_rot_matrix, get_3d_vertex_dir, get_2d_vertex

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
        rv3d           = context.space_data.region_3d
        self._view_rot = rv3d.view_rotation.copy()
        self._view_mat = rv3d.view_matrix.copy()
        self._pers_mat = rv3d.perspective_matrix.copy()
        self._view_pers = rv3d.view_perspective
        self._is_perspective = rv3d.is_perspective
        self._region = ViewRegion(context.region)

    @property
    def region(self):
        return self._region

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
        self._vertices = []
        self._is_moving = False
        self._move_offset = 0.0
        self._is_rotating = False
        self._is_extruding = False
        self._rotation = 0.0
        self._view_context = None 

    def is_none(self):
        return self._state is ShapeState.NONE
 
    def is_processing(self):
        return self._state is ShapeState.PROCESSING

    def is_created(self):
        return self._state is ShapeState.CREATED

    def is_moving(self):
        return self._is_moving

    def is_rotating(self):
        return self._is_rotating

    def is_extruding(self):
        return self._is_extruding

    def get_dir(self):
        view_rot = self._view_context.view_rotation
        
        return get_view_direction_by_rot_matrix(view_rot)

    def get_view_context(self):
        return self._view_context

    def set_view_context(self, value):
        self._view_context = value

    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, value):
        self._vertices = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    def add_vertex(self, vertex):
        self._vertices.append(vertex)

    def reset(self):
        self._vertices.clear()     
        self._state = ShapeState.NONE

    def close(self):            
        return False

    def get_vertices_copy(self, mouse_pos = None):
        result = self._vertices.copy()

        return result

    def start_move(self, mouse_pos):
        if self.is_created():
            self._is_moving = True
            self._move_offset = mouse_pos
            return True
        return False

    def stop_move(self, context):
        self._is_moving = False
        self._move_offset = 0.0

    def start_rotate(self, mouse_pos, context):
        return False

    def stop_rotate(self, context):
        self._is_rotating = False
        self._rotation = 0.0

    def start_extrude(self, mouse_pos, context):
        return False

    def stop_extrude(self, context):
        self._is_extruding = False

    def handle_mouse_move(self, mouse_pos_2d, mouse_pos_3d, event, context):
        if self.is_created() and self._is_moving:
            diff = mouse_pos_3d - self._move_offset
            self._vertices = [vertex + diff for vertex in self._vertices]           
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

    def get_text(self, context):
        pass

    def draw_points(self):
        return True