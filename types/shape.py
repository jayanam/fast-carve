from enum import Enum

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
        if len(self._vertices) > 1:
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

    def handle_mouse_move(self, mouse_pos):
        if self.is_processing():
            return True

        return False

    def handle_mouse_press(self, mouse_pos):

        if not self.is_created():
            self.add_vertex(mouse_pos)
            self.state = ShapeState.PROCESSING
            return True

        return False

    def handle_apply(self):
        if self.is_processing():
            if not self.close():
                self.reset()

        # The shape is created, apply the shape (e.g. create object)
        elif self.is_created():
            return True

        return False
