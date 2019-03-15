from .widgets . bl_ui_draw_op import *
from .widgets . bl_ui_label import * 
from .widgets . bl_ui_button import *
from .widgets . bl_ui_slider import *
from .widgets . bl_ui_up_down import *
from .widgets . bl_ui_drag_panel import *
from .widgets . bl_ui_draw_op import *

# Array mode operator
class FC_Array_Mode_Operator(BL_UI_OT_draw_operator):
    bl_idname = "object.fc_array_mode_op"
    bl_label = "Array Mode Operator"
    bl_description = "Array modifier utility"
    bl_options = {"REGISTER", "UNDO"}

    def __init__(self):
        
        super().__init__()
            
        self.panel = BL_UI_Drag_Panel(0, 0, 300, 110)
        self.panel.set_bg_color((0.1, 0.1, 0.1, 0.9))

        self.lbl_item_count = BL_UI_Label(20, 13, 40, 15)
        self.lbl_item_count.set_text("Item count:")
        self.lbl_item_count.set_text_size(14)
        self.lbl_item_count.set_text_color((0.9, 0.9, 0.9, 1.0))

        self.ud_item_count = BL_UI_Up_Down(110, 15)
        self.ud_item_count.set_color((0.2, 0.8, 0.8, 0.8))
        self.ud_item_count.set_hover_color((0.2, 0.9, 0.9, 1.0))
        self.ud_item_count.set_min(1.0)
        self.ud_item_count.set_max(50.0)
        self.ud_item_count.set_value(2.0)
        self.ud_item_count.set_decimals(0)
        self.ud_item_count.set_value_change(self.on_item_count_value_change)

        self.lbl_item_dist = BL_UI_Label(20, 62, 50, 15)
        self.lbl_item_dist.set_text("Distance:")
        self.lbl_item_dist.set_text_size(14)
        self.lbl_item_dist.set_text_color((0.9, 0.9, 0.9, 1.0))

        self.sl_item_distance = BL_UI_Slider(110, 60, 150, 30)
        self.sl_item_distance.set_color((0.2, 0.8, 0.8, 0.8))
        self.sl_item_distance.set_hover_color((0.2, 0.9, 0.9, 1.0))
        self.sl_item_distance.set_min(1.0)
        self.sl_item_distance.set_max(10.0)
        self.sl_item_distance.set_value(2.0)
        self.sl_item_distance.set_decimals(1)
        self.sl_item_distance.set_value_change(self.on_item_distance_change)

    def on_invoke(self, context, event):

        # Add new widgets here (TODO: perhaps a better, more automated solution?)
        widgets_panel = [self.lbl_item_count, self.ud_item_count, self.lbl_item_dist, self.sl_item_distance]
        widgets =       [self.panel]

        widgets += widgets_panel

        self.init_widgets(context, widgets)

        self.panel.add_widgets(widgets_panel)

        # Open the panel at the mouse location
        self.panel.set_location(event.mouse_x, 
                                context.area.height - event.mouse_y + 20)

    def on_item_count_value_change(self, up_down, value):
        active_obj = bpy.context.view_layer.objects.active
        if active_obj is not None:
            mod_array = active_obj.modifiers.get("Array")
            mod_array.count = value

    def on_item_distance_change(self, slider, value):
        active_obj = bpy.context.view_layer.objects.active
        if active_obj is not None:
            mod_array = active_obj.modifiers.get("Array")
            mod_array.relative_offset_displace[1] = value