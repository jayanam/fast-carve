from enum import Enum

from math import sin, cos, pi

from mathutils import Vector

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
        self._dir = Vector((0,0,0))

    def is_none(self):
        return self._state is ShapeState.NONE
 
    def is_processing(self):
        return self._state is ShapeState.PROCESSING

    def is_created(self):
        return self._state is ShapeState.CREATED

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

    def stop_move(self):
        self._is_moving = False
        self._move_offset = 0.0

    def handle_mouse_move(self, mouse_pos, event, context):
        if self.is_created() and self._is_moving:
            diff = mouse_pos - self._move_offset
            self._vertices = [vertex + diff for vertex in self._vertices]           
            self._move_offset = mouse_pos
            return True
        return False

    def handle_mouse_press(self, mouse_pos, event, context):
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

class Polyline_Shape(Shape):

    def can_close(self):
        return len(self._vertices) > 1

    def close(self):
            
        if self.can_close():
            self._state = ShapeState.CREATED
            return True
            
        return False

    def get_vertices_copy(self, mouse_pos = None):
        result = self._vertices.copy()

        if mouse_pos is not None and self.is_processing():
            result.append(mouse_pos)

        return result


    def handle_mouse_press(self, mouse_pos, event, context):

        if (self.is_none() and event.ctrl) or (self.is_processing() and not event.ctrl):

            self.add_vertex(mouse_pos)
            self.state = ShapeState.PROCESSING
            return False

        elif self.is_processing() and event.ctrl and self.can_close():
            self.add_vertex(mouse_pos)
            self.close()
            return False

        elif self.is_created() and event.ctrl:
            return True

        return False

    def handle_mouse_move(self, mouse_pos, event, context):

        if self.is_processing():
            return True

        result = super().handle_mouse_move(mouse_pos, event, context)

        return result

    def get_text(self, context):
        text = "{0} | Mode (M): {1} | Primitive (P): {2} | {3}"

        keyboard = "Esc: Exit"
        mouse_action = "Add line: Ctrl + Left click"
        p_type = "Polyline"

        if self.is_created():
            mouse_action = "Apply: Ctrl + Left Click"
            keyboard = "Esc: Undo | G: Move"
        
        if self.is_processing():
            keyboard = "Esc: Undo"
            if self.can_close():
                mouse_action = "Close Shape: Ctrl + Left Click"
            else:
                mouse_action = "Add line: Left Click"
            
        return text.format(mouse_action, context.scene.bool_mode, p_type, keyboard)

class Circle_Shape(Shape):

    def __init__(self):
        super().__init__()
        self._center = None
        self._radius = 0

    def handle_mouse_move(self, mouse_pos, event, context):

        if self.is_processing():

            # Distance center to mouse pos
            self._radius = (self._center - mouse_pos).length

            self.create_circle(context)
            return True
           
        result = super().handle_mouse_move(mouse_pos, event, context)

        return result

    def create_circle(self, context):
        rv3d      = context.space_data.region_3d
        view_rot  = rv3d.view_rotation

        segments = 32
        mul = (1.0 / (segments - 1)) * (pi * 2)
        points = [(sin(i * mul) * self._radius, cos(i * mul) * self._radius, 0) 
        for i in range(segments)]

        self._vertices = [view_rot @ Vector(point) + 
                          self._center for point in points]


    def handle_mouse_press(self, mouse_pos, event, context):

        if self.is_none() and event.ctrl:

            self._center = mouse_pos
            self.state = ShapeState.PROCESSING
            return False

        elif self.is_processing():

            self.state = ShapeState.CREATED
            return False

        elif self.is_created() and event.ctrl:
            return True

        return False

    def draw_points(self):
        return False

    def get_text(self, context):
        text = "{0} | Mode (M): {1} | Primitive (P): {2} | {3}"

        keyboard = "Esc: Exit"
        mouse_action = "Set center: Ctrl + Left click"
        p_type = "Circle"

        if self.is_created():
            keyboard = "Esc: Undo | G: Move"
            mouse_action = "Apply: Ctrl + Left Click"
   
        if self.is_processing():
            mouse_action = "Create: Left click"
            keyboard = "Esc: Undo"

        return text.format(mouse_action, context.scene.bool_mode, p_type, keyboard)

class Rectangle_Shape(Shape):
    
    def __init__(self):
        super().__init__()
        self._vertex1 = None
        self._vertex3 = None

    def handle_mouse_move(self, mouse_pos, event, context):

        if self.is_processing():

            self._vertex3 = mouse_pos
            self.create_rect(context)
            return True

        result = super().handle_mouse_move(mouse_pos, event, context)

        return result


    def create_rect(self, context):
        rv3d      = context.space_data.region_3d
        view_rot  = rv3d.view_rotation

        self._vertices.clear()
        self._vertices.append(self._vertex1)
        vertex2 = self._vertex1.copy()
        vertex2[2] = self._vertex3[2]

        vertex4 = self._vertex3.copy()
        vertex4[2] = self._vertex1[2]
        
        self._vertices.extend([vertex2, self._vertex3, vertex4])
        
    def handle_mouse_press(self, mouse_pos, event, context):

        if self.is_none() and event.ctrl:

            self._vertex1 = mouse_pos
            self.state = ShapeState.PROCESSING
            return False

        elif self.is_processing():
            self.state = ShapeState.CREATED
            return False

        elif self.is_created() and event.ctrl:
            return True

        return False

    def draw_points(self):
        return True

    def get_text(self, context):
        text = "{0} | Mode (M): {1} | Primitive (P): {2} | {3}"

        keyboard = "Esc: Exit"
        mouse_action = "Set point 1: Ctrl + Left click"
        p_type = "Rectangle"

        if self.is_created():
            keyboard = "Esc: Undo | G: Move"
            mouse_action = "Apply: Ctrl + Left Click"
   
        if self.is_processing():
            mouse_action = "Set point 2: Left click"
            keyboard = "Esc: Undo"

        return text.format(mouse_action, context.scene.bool_mode, p_type, keyboard)

