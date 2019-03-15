from . bl_ui_widget import *

import blf
import bpy

class BL_UI_Button(BL_UI_Widget):
    
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.__text_color        = (1.0, 1.0, 1.0, 1.0)
        self.__hover_bg_color    = (0.5, 0.5, 0.5, 1.0)
        self.__select_bg_color   = (0.7, 0.7, 0.7, 1.0)
        
        self.__text = "Button"
        self.__text_size = 16
        self.__state = 0
        self.__textpos = (x, y)
        self.__image = None
        self.__image_size = (24, 24)
        self.__image_position = (4, 2)

    def set_text_color(self, color):
        self.__text_color = color

    @property
    def text(self):
        return self.__text
    
    def set_text(self, text):
        self.__text = text
            
    def set_text_size(self, size):
        self.__text_size = size
        
    def set_hover_bg_color(self, color):
        self.__hover_bg_color = color
        
    def set_select_bg_color(self, color):
        self.__select_bg_color = color

    def set_image_size(self, imgage_size):
        self.__image_size = imgage_size

    def set_image_position(self, image_position):
        self.__image_position = image_position

    def set_image(self, rel_filepath):
        try:
            self.__image = bpy.data.images.load(rel_filepath, check_existing=True)   
            self.__image.gl_load()
        except:
            pass

    def update(self, x, y):        
        super().update(x, y)
        self.__textpos = [x, y]

        area_height = self.get_area_height()
        
        y_screen_flip = area_height - self.y_screen
        
        off_x, off_y =  self.__image_position
        sx, sy = self.__image_size
        
        # bottom left, top left, top right, bottom right
        vertices = (
                    (self.x_screen + off_x, y_screen_flip - off_y), 
                    (self.x_screen + off_x, y_screen_flip - sy - off_y), 
                    (self.x_screen + off_x + sx, y_screen_flip - sy - off_y),
                    (self.x_screen + off_x + sx, y_screen_flip - off_x))
        
        self.shader_img = gpu.shader.from_builtin('2D_IMAGE')
        self.batch_img = batch_for_shader(self.shader_img, 'TRI_FAN', 
        { "pos" : vertices, 
          "texCoord": ((0, 1), (0, 0), (1, 0), (1, 1)) 
        },)
        
    def draw(self):

        area_height = self.get_area_height()

        self.shader.bind()
        
        self.set_colors()
        
        bgl.glEnable(bgl.GL_BLEND)

        self.batch_panel.draw(self.shader) 

        self.draw_image()   

        bgl.glDisable(bgl.GL_BLEND)

        # Draw text
        self.draw_text(area_height)

    def set_colors(self):
        color = self.bg_color
        text_color = self.__text_color

        # pressed
        if self.__state == 1:
            color = self.__select_bg_color

        # hover
        elif self.__state == 2:
            color = self.__hover_bg_color

        self.shader.uniform_float("color", color)

    def draw_text(self, area_height):
        blf.size(0, self.__text_size, 72)
        size = blf.dimensions(0, self.__text)

        textpos_y = area_height - self.__textpos[1] - (self.height + size[1]) / 2.0
        blf.position(0, self.__textpos[0] + (self.width - size[0]) / 2.0, textpos_y + 1, 0)

        r, g, b, a = self.__text_color
        blf.color(0, r, g, b, a)

        blf.draw(0, self.__text)

    def draw_image(self):
        if self.__image is not None:
            try:
                bgl.glActiveTexture(bgl.GL_TEXTURE0)
                bgl.glBindTexture(bgl.GL_TEXTURE_2D, 
                self.__image.bindcode)

                self.shader_img.bind()
                self.shader_img.uniform_int("image", 0)
                self.batch_img.draw(self.shader_img) 
                return True
            except:
                pass

        return False     
        
    def set_mouse_down(self, mouse_down_func):
        self.mouse_down_func = mouse_down_func   
                 
    def mouse_down(self, x, y):    
        if self.is_in_rect(x,y):
            self.__state = 1
            try:
                self.mouse_down_func(self)
            except:
                pass
                
            return True
        
        return False
    
    def mouse_move(self, x, y):
        if self.is_in_rect(x,y):
            if(self.__state != 1):
                
                # hover state
                self.__state = 2
        else:
            self.__state = 0
 
    def mouse_up(self, x, y):
        if self.is_in_rect(x,y):
            self.__state = 2
        else:
            self.__state = 0