from .shape import *

class Circle_Shape(Shape):

    def __init__(self):
        super().__init__()
        self._center = None
        self._radius = 0
        self._mouse_start_3d = None
        self._segments = 24

    def handle_mouse_wheel(self, inc, context):
        if self.is_processing():
            self._segments += inc
            if self._segments < 3:
                self._segments = 3

            self.build_actions()
            self.create_circle(context)
            return True

        return False

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

        segments = self._segments + 1
        mul = (1.0 / (segments - 1)) * (pi * 2)
        points = [(sin(i * mul) * self._radius, cos(i * mul) * self._radius, 0) 
        for i in range(segments)]

        rot_mat = view_rot
        offset = Vector((0,0,0))

        if self._snap_to_target and self._normal != None:
            rot_mat = self._normal.to_track_quat('Z', 'X').to_matrix()
            offset = self._normal.normalized() * 0.01

        self._vertices = [rot_mat @ Vector(point) + 
                          self._center +  offset for point in points]

        self._vertices_2d = [get_2d_vertex(context, vertex) for vertex in self._vertices]

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

    def get_center(self, mouse_pos_3d, context):
        if context.scene.center_type == "Mouse":
            return mouse_pos_3d
        else:
            return context.scene.cursor.location

    def build_actions(self):
        super().build_actions()
        bool_mode = bpy.context.scene.bool_mode
        center_type = bpy.context.scene.center_type

        self.add_action(Action(self.get_prim_id(),  "Primitive",          "Circle"),    None)
        self.add_action(Action("M",                 "Mode",               bool_mode),   None)
        self.add_action(Action("G",                 "Move",               ""),          ShapeState.CREATED)
        self.add_action(Action("E",                 "Extrude",            ""),          ShapeState.CREATED)
        self.add_action(Action("C",                 "Center",             center_type), ShapeState.NONE)
        self.add_action(Action("Left Click",        "Create",             ""),          ShapeState.PROCESSING)
        self.add_action(Action("Ctrl + Left Click", "Start",              ""),          ShapeState.NONE)
        self.add_action(Action("Ctrl + Left Click", "Apply",              ""),          ShapeState.CREATED)
        self.add_action(Action("Mouse wheel",       "Segments",           str(self._segments)), ShapeState.PROCESSING)
        self.add_action(Action("Esc",               self.get_esc_title(), ""),          None)