from .shape import *

class Curve_Shape(Shape):

    def __init__(self):
        super().__init__()
        self._mat_rot = [None, None]

    def can_close(self):
        return len(self._vertices) == 2

    def close(self):
            
        if self.can_close():
            self.state = ShapeState.CREATED
            return True
            
        return False

    def connected_shape(self):
        return False

    def get_vertices_copy(self, mouse_pos = None):
        result = self._vertices.copy()

        if mouse_pos is not None and self.is_processing():
            result.append(mouse_pos)

        return result

    def get_start_point(self):
        if(self.is_created()):
            return self._vertices[0]
        return None

    def get_end_point(self):
        if(self.is_created()):
            return self._vertices[1]
        return None

    def get_start_rotation(self):
        return self._mat_rot[0]

    def get_end_rotation(self):
        return self._mat_rot[1]

    def set_rotation(self, mat_rot):

        if self.is_none():
            self._mat_rot[0] = mat_rot
        else:
            self._mat_rot[1] = mat_rot 

    def handle_mouse_press(self, mouse_pos_2d, mouse_pos_3d, event, context):

        if mouse_pos_3d is None:
            return False

        if self.is_none() and event.ctrl:

            self.add_vertex(mouse_pos_3d)
            self._vertices_2d.append(get_2d_vertex(context, mouse_pos_3d))
            self.state = ShapeState.PROCESSING
            return False

        elif self.is_processing() and event.ctrl:
            self.add_vertex(mouse_pos_3d)
            self._vertices_2d.append(get_2d_vertex(context, mouse_pos_3d))
            self.close()
            return False

        elif self.is_created() and event.ctrl:
            return True

        return False

    def handle_mouse_move(self, mouse_pos_2d, mouse_pos_3d, event, context):

        if self.is_processing():
            return True

        result = super().handle_mouse_move(mouse_pos_2d, mouse_pos_3d, event, context)

        return result

    def build_actions(self):
        super().build_actions()
        bool_mode = bpy.context.scene.bool_mode
        self.add_action(Action(self.get_prim_id(),  "Primitive",          "Curve"),  None)
        self.build_move_action()
        self.add_action(Action("Ctrl + Left Click", "Set Startpoint",     ""),       ShapeState.NONE)
        self.add_action(Action("Ctrl + Left Click", "Set Endpoint",       ""),       ShapeState.PROCESSING)
        self.add_action(Action("Ctrl + Left Click", "Apply",              ""),       ShapeState.CREATED)
        self.add_action(Action("Left Drag",         "Move points",        ""),       ShapeState.CREATED)
        self.add_action(Action("Esc",               self.get_esc_title(), ""),       None)