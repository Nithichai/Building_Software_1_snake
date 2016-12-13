import pygame
import random
from Object import Object

class Apple(Object):  # Apple is object
    
    def __init__(self, x, y, tile_mng, color, typ):  # Define value
        Object.__init__(self, x, y, tile_mng, color, typ)  # Link to mother class
        self.eaten = False
    
    def restart(self):  # Start snake by set apple's x, y and set not eaten
        self.set_x(random.randrange(0, self.tile_mng.get_nw_tile())) 
        self.set_y(random.randrange(0, self.tile_mng.get_nh_tile()))
        self.eaten = False
    
    def update(self):  # Update Apple
        pass
    
    def render(self, game_display):  # Render Apple
        if not self.eaten:  # Not eaten state -> draw apple
            pygame.draw.rect(game_display, self.color, pygame.Rect(int(self.get_x()), int(self.get_y()), \
                                                                   int(self.get_width()), int(self.get_height())))
    
    def get_eaten(self):
        return self.eaten
    
    def set_eaten(self, eaten):  # Set eaten
        self.eaten = eaten
