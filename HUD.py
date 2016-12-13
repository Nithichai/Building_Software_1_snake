import pygame

black = (0, 0, 0)
orange = (255, 255, 0)

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
        pygame.draw.rect(game_display, orange, pygame.Rect(int(x), int(y), int(w * gauge_per), int(h)))