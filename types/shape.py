from enum import Enum

from math import sin, cos, pi, radians

from mathutils import Vector, geometry

from ..utils.fc_view_3d_utils import get_3d_vertex, get_3d_vertex_dir, get_2d_vertex

class ShapeState(Enum):
    NONE = 0
    PROCESSING = 1
    CREATED = 2

class Shape:

    def __init__(self):
        self._state = ShapeState.NONE
        self._vertices = []
        self._is_moving = False
        self._move_offset = 0.0
        self._is_rotating = False
        self._rotation = 0.0

        self._dir = Vector((0,0,0))

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

    def get_dir(self):
        return self._dir

    def set_dir(self, value):
        self._dir = value

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