from .shape import *

class Polyline_Shape(Shape):

    def can_close(self):
        return len(self._vertices) > 1

    def close(self):
            
        if self.can_close():
            self.state = ShapeState.CREATED
            return True
            
        return False

    def get_vertices_copy(self, mouse_pos = None):
        result = self._vertices.copy()

        if mouse_pos is not None and self.is_processing():
            result.append(mouse_pos)

        return result


    def handle_mouse_press(self, mouse_pos_2d, mouse_pos_3d, event, context):

        if mouse_pos_3d is None:
            return False

        if (self.is_none() and event.ctrl) or (self.is_processing() and not event.ctrl):

            self.add_vertex(mouse_pos_3d)
            self._vertices_2d.append(get_2d_vertex(context, mouse_pos_3d))
            self.state = ShapeState.PROCESSING
            return False

        elif self.is_processing() and event.ctrl and self.can_close():
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
        self.add_action(Action("P",                 "Primitive",          "Polyline"),  ShapeState.NONE)
        self.add_action(Action("M",                 "Mode",               bool_mode),   None)
        self.add_action(Action("G",                 "Move",               ""),          ShapeState.CREATED)
        self.add_action(Action("E",                 "Extrude",            ""),          ShapeState.CREATED)
        self.add_action(Action("Left Click",        "Add line",           ""),          ShapeState.PROCESSING)
        self.add_action(Action("Ctrl + Left Click", "Start",              ""),          ShapeState.NONE)

        if self.can_close():
            self.add_action(Action("Ctrl + Left Click", "Close shape",    ""),          ShapeState.PROCESSING)

        self.add_action(Action("Ctrl + Left Click", "Apply",              ""),          ShapeState.CREATED)
        self.add_action(Action("Esc",               self.get_esc_title(), ""),          None)      

    def get_text(self, context):
        text = "{0} | Mode (M): {1} | Primitive (P): {2} | {3}"

        keyboard = "Esc: Exit"
        mouse_action = "Add line: Ctrl + Left click"
        p_type = "Polyline"

        if self.is_created():
            mouse_action = "Apply: Ctrl + Left Click"
            keyboard = "Esc: Undo | G: Move | E: Extrude"
        
        if self.is_processing():
            keyboard = "Esc: Undo"
            if self.can_close():
                mouse_action = "Close Shape: Ctrl + Left Click"
            else:
                mouse_action = "Add line: Left Click"
            
        return text.format(mouse_action, context.scene.bool_mode, p_type, keyboard)