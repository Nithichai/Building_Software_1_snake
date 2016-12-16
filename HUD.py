import pygame
import math

black = (0, 0, 0)
white = (255, 255, 255)
orange = (255, 255, 0)
red = (255, 0, 0)

class HUD():
    
    def __init__(self):
        pygame.init()
        
    def time_hud(self, game_display, time, x, y):
        font = pygame.font.SysFont(None, 60)
        text = font.render(str(time), True, black)
        text_rect = text.get_rect(center=(x, y))
        game_display.blit(text, text_rect)
    
    def score_hud(self, game_display, score, x, y):
        font = pygame.font.SysFont(None, 30)
        text = font.render("SCORE : " + str(score), True, black)
        text_rect = text.get_rect(center=(x, y))
        game_display.blit(text, text_rect)
    
    def gauge_hud(self, game_display, gauge_per, x, y, w, h):
        font = pygame.font.SysFont(None, 20)
        text = font.render(str(int(gauge_per * 100)), True, black)
        text_rect = text.get_rect(center=(x - x/10, y))
        game_display.blit(text, text_rect)
        pygame.draw.rect(game_display, orange, pygame.Rect(int(x), int(y), int(w * gauge_per), int(h)))
        
    def dead_hud(self, game_display, time, delay, x, y, w, h):
        font = pygame.font.SysFont(None, 30)
        text = font.render("YOU ARE DEAD", True, red)
        text_rect = text.get_rect(center=(x, y))
        game_display.blit(text, text_rect)
        pygame.draw.arc(game_display, red, (int(x) - int(w/2), int(y) - int(h/2), int(w), int(h)), 0, time * 2 * math.pi / delay, 10)