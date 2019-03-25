from .shape import *

class Circle_Shape(Shape):

    def __init__(self):
        super().__init__()
        self._center = None
        self._radius = 0
        self._mouse_start_3d = None

    def handle_mouse_move(self, mouse_pos_2d, mouse_pos_3d, event, context):

        if self.is_processing():

            # Distance center to mouse pos
            self._radius = (self._mouse_start_3d - mouse_pos_3d).length

            self.create_circle(context)
            return True
           
        result = super().handle_mouse_move(mouse_pos_2d, mouse_pos_3d, event, context)

        return result

    def create_circle(self, context):

        from mathutils import Matrix

        rv3d      = context.space_data.region_3d
        view_rot  = rv3d.view_rotation

        segments = 32
        mul = (1.0 / (segments - 1)) * (pi * 2)
        points = [(sin(i * mul) * self._radius, cos(i * mul) * self._radius, 0) 
        for i in range(segments)]

        rot_mat = view_rot

        if self._snap_to_target:
            rot_mat = self._normal.to_track_quat('Z', 'X').to_matrix()

        self._vertices = [rot_mat @ Vector(point) + 
                          self._center for point in points]

        self._vertices_2d = [get_2d_vertex(context, vertex) for vertex in self._vertices]


    def get_center(self, mouse_pos_3d, context):
        if context.scene.center_type == "Mouse":
            return mouse_pos_3d
        else:
            return context.scene.cursor.location

    def handle_mouse_press(self, mouse_pos_2d, mouse_pos_3d, event, context):

        if mouse_pos_3d is None:
            return False

        if self.is_none() and event.ctrl:

            self._center = self.get_center(mouse_pos_3d, context)

            self._mouse_start_3d = mouse_pos_3d.copy()

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

    def can_set_center_type(self):
        return True

    def get_text(self, context):
        text = "{0} {1} | Mode (M): {2} | Primitive (P): {3} | {4}"

        keyboard = "Esc: Exit"
        mouse_action = "Start: Ctrl + Left click | Center (C):"
        p_type = "Circle"

        if self.is_created():
            keyboard = "Esc: Undo | G: Move | E: Extrude"              
            mouse_action = "Apply: Ctrl + Left Click"
   
        if self.is_processing():
            mouse_action = "Create: Left click"
            keyboard = "Esc: Undo"

        return text.format(mouse_action, context.scene.center_type, context.scene.bool_mode, p_type, keyboard)