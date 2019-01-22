from .shape import *

class Circle_Shape(Shape):

    def __init__(self):
        super().__init__()
        self._center = None
        self._radius = 0

    def handle_mouse_move(self, mouse_pos_2d, mouse_pos_3d, event, context):

        if self.is_processing():

            # Distance center to mouse pos
            self._radius = (self._center - mouse_pos_3d).length

            self.create_circle(context)
            return True
           
        result = super().handle_mouse_move(mouse_pos_2d, mouse_pos_3d, event, context)

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

        self._vertices_2d = [get_2d_vertex(context, vertex) for vertex in self._vertices]


    def handle_mouse_press(self, mouse_pos_2d, mouse_pos_3d, event, context):

        if self.is_none() and event.ctrl:

            self._center = mouse_pos_3d
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
            keyboard = "Esc: Undo | G: Move | E: Extrude"              
            mouse_action = "Apply: Ctrl + Left Click"
   
        if self.is_processing():
            mouse_action = "Create: Left click"
            keyboard = "Esc: Undo"

        return text.format(mouse_action, context.scene.bool_mode, p_type, keyboard)