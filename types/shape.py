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

    def is_none(self):
        return self._state is ShapeState.NONE

    def is_processing(self):
        return self._state is ShapeState.PROCESSING

    def is_created(self):
        return self._state is ShapeState.CREATED

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

    def handle_mouse_move(self, mouse_pos, event, context):
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

    def get_title(self, context):
        pass

    def get_text(self, context):
        pass

class Polyline_Shape(Shape):

    def can_close(self):
        return len(self._vertices) > 1

    def close(self):
            
        if self.can_close():
            if self._vertices[0] is not self._vertices[-1]:
                self._vertices.append(self._vertices[0])
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

        return False

    def get_title(self, context):
        return "Polyline"

    def get_text(self, context):
        text = "{0} | Mode: {1} | Type: {2} | Esc : {3}"

        escape_action = "Exit"
        mouse_action = "Add line: Ctrl + Left click"
        p_type = "Polyline"

        if self.is_created():
            mouse_action = "Apply: Ctrl + Left Click"
            escape_action = "Undo"
        
        if self.is_processing():
            escape_action = "Undo"
            if self.can_close():
                mouse_action = "Close Shape: Ctrl + Left Click"
            else:
                mouse_action = "Add line: Left Click"
            
        return text.format(mouse_action, context.scene.bool_mode, p_type, escape_action)

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

        return False

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

    def get_title(self, context):
        return "Circle"

    def get_text(self, context):
        text = "{0} | Mode: {1} | Type: {2} | Esc : {3}"

        escape_action = "Exit"
        mouse_action = "Set center: Ctrl + Left click"
        p_type = "Circle"

        if self.is_created():
            escape_action = "Undo"
            mouse_action = "Apply: Ctrl + Left Click"
   
        if self.is_processing():
            mouse_action = "Create: Left click"
            escape_action = "Undo"

        return text.format(mouse_action, context.scene.bool_mode, p_type, escape_action)
