class Object() :
    
    def __init__(self, x, y, tile_mng, color, typ):
        self.tile_mng = tile_mng
        self.width = tile_mng.get_sizew_tile()
        self.height = tile_mng.get_sizeh_tile()
        self.x = x * self.width
        self.y = y * self.height
        self.color = color
        self.typ = typ
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_x_n(self):
        return int(self.x / self.width)
    
    def get_y_n(self):
        return int(self.y / self.height)
    
    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    
    def get_tile_mng(self):
        return self.tile_mng
    
    def get_color(self):
        return self.color
    
    def get_type(self):
        return self.typ

    def set_x(self, x):
        self.x = x * self.get_width()

    def set_y(self, y):
        self.y = y * self.get_height()
    
    def set_width(self, width):
        self.width = width
    
    def set_height(self, height):
        self.height = height
        
    def set_tile_mng(self, tile_mng):
        self.tile_mng = tile_mng
    
    def set_color(self):
        self.color = color
    
    def set_type(self, typ):
        self.typ = typ