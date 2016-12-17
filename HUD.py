import pygame
import math

black = (0, 0, 0)
white = (255, 255, 255)
orange = (255, 255, 0)
red = (255, 0, 0)

class HUD():
    
    # Start hud
    def __init__(self):
        pygame.init()   # Set pygame
        
    def time_hud(self, game_display, time, x, y):
        font = pygame.font.SysFont(None, 60)        # Set font style
        text = font.render(str(time), True, black)  # Set time text
        text_rect = text.get_rect(center=(x, y))    # Set postion
        game_display.blit(text, text_rect)          # Set text in postion
    
    def score_hud(self, game_display, score, x, y):
         # Set score text
        font = pygame.font.SysFont(None, 30)       
        text = font.render("SCORE : " + str(score), True, black)
        text_rect = text.get_rect(center=(x, y))
        game_display.blit(text, text_rect)
    
    def gauge_hud(self, game_display, gauge_per, x, y, w, h):
        # Set gauge percent text
        font = pygame.font.SysFont(None, 20)
        text = font.render(str(int(gauge_per * 100)), True, black)
        text_rect = text.get_rect(center=(x - x/10, y))
        game_display.blit(text, text_rect)
        pygame.draw.rect(game_display, orange, pygame.Rect(int(x), int(y), int(w * gauge_per), int(h))) # Set rectangle of gauge
        
    def dead_hud(self, game_display, time, delay, x, y, w, h):
        # Set "You are dead" text
        font = pygame.font.SysFont(None, 30)    
        text = font.render("YOU ARE DEAD", True, red)
        text_rect = text.get_rect(center=(x, y))
        game_display.blit(text, text_rect)
        pygame.draw.arc(game_display, red, (int(x) - int(w/2), int(y) - int(h/2), int(w), int(h)), 0, time * 2 * math.pi / delay, 10)   # Set arc of gauge