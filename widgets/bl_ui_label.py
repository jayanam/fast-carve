from . bl_ui_widget import *

import blf

class BL_UI_Label(BL_UI_Widget):
    
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.text_color        = (1.0, 1.0, 1.0, 1.0)
        
        self.text = "Label"
        self.text_size = 16

    def set_text_color(self, color):
        self.text_color = color
    
    def set_text(self, text):
        self.text = text
            
    def set_text_size(self, size):
        self.text_size = size

    def is_in_rect(self, x, y):
        return False
        
    def draw(self):
        area_height = self.get_area_height()

        blf.size(0, self.text_size, 72)
        size = blf.dimensions(0, self.text)
    
        textpos_y = area_height - self.y_screen - self.height
        blf.position(0, self.x_screen, textpos_y, 0)

        r, g, b, a = self.text_color

        blf.color(0, r, g, b, a)
            
        blf.draw(0, self.text)