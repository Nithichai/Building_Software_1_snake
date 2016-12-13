import pygame
import time
from TileManager import TileManager
from Apple import Apple
from Snake import Snake
from CounterTime import CounterTime
from ClientManager import ClientManager
from HUD import HUD

SNAKE = "s"
APPLE = "a"

class BoardManager():
    
    def  __init__(self, nw_tile, nh_tile):  # Define value
        self.nw_tile = nw_tile
        self.nh_tile = nh_tile
        
        self.number_body = 3
        self.score = 0
        
        self.db_save_size = 6
        self.id = 0
        self.type = 1
        self.x = 2
        self.y = 3
        self.s = 4
        self.t = 5
        
        self.enemy_dict = {}
        self.client_state_dict = {'OK':0, 'notNStart':1, 'notNExit':2}
        self.client_state = self.client_state_dict['notNStart']
        self.play_state = False
        self.game_time = 0
        
        self.tile_mng = TileManager(width, height, self.nw_tile, self.nh_tile)  # Set TileManager
        self.snake = Snake(1, 1, self.tile_mng, green, SNAKE, raw_input("Enter : "), self.number_body)
        self.apple = Apple(0, 0, self.tile_mng, red, 0)
        self.hud = HUD()
        
    def update(self):  # Update board
        for event in pygame.event.get():  # Check all event
            if event.type == pygame.QUIT:  # Click Quit to quit program
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_LEFT and not self.snake.get_move_list('right'):
                    self.snake.set_left()
                elif event.key == pygame.K_RIGHT and not self.snake.get_move_list('left'):
                    self.snake.set_right()
                elif event.key == pygame.K_UP and not self.snake.get_move_list('down'):
                    self.snake.set_up()
                elif event.key == pygame.K_DOWN and not self.snake.get_move_list('up'):
                    self.snake.set_down()
                elif event.key == pygame.K_x:
                    self.snake.snake_slide(self.snake.get_move(), self.apple)
                elif event.key == pygame.K_c:
                    self.snake.snake_running()
        
        x_pos_ls = [int(self.snake.get_x_pos()[i] / self.tile_mng.get_sizew_tile()) for i in range(self.snake.get_number_body())]
        y_pos_ls = [int(self.snake.get_y_pos()[i] / self.tile_mng.get_sizeh_tile ())for i in range(self.snake.get_number_body())]
        x_pos_n = self.client.pos_pattern(x_pos_ls)
        y_pos_n = self.client.pos_pattern(y_pos_ls)
        pattern = self.client.set_pattern(self.snake.get_id(), [self.snake.get_type(), x_pos_n, y_pos_n, self.score, 0])
        
        if self.client_state == self.client_state_dict['OK']:
            self.snake.snake_eat_apple(self.apple)
            self.snake.update()
            if self.apple.get_eaten():
                pattern = "eaten"
                self.apple.set_eaten(False)
        self.client.send(pattern)
        
        data, addr = self.client.recv()
        if data == "notNStart" :
            self.client_state = self.client_state_dict['notNStart']
        elif data == "notNExit" :
            self.client_state = self.client_state_dict['notNExit']
        else :
            self.client_state = self.client_state_dict['OK']
            split_list = self.client.split(data)    
            for ls in split_list :
                self.game_time = int(ls[self.t])
                if ls[self.id] == "*" :
                    self.apple = Apple(int(ls[self.x]), int(ls[self.y]), self.tile_mng, red, str(ls[self.type]))
                elif ls[self.id] != self.snake.get_id() and ls[self.id] != "*":
                    self.enemy_dict[ls[self.id]] = Snake(0, 0, self.tile_mng, blue, ls[self.type], ls[self.id], 0)
                    x_pos = self.client.pos_split(ls[self.x])
                    y_pos = self.client.pos_split(ls[self.y])
                    x_list = [int(x_pos[i] * self.tile_mng.get_sizew_tile()) for i in range(len(x_pos))]
                    y_list = [int(y_pos[i] * self.tile_mng.get_sizeh_tile()) for i in range(len(y_pos))]
                    self.enemy_dict[ls[self.id]].set_pos(x_list, y_list)
         
    def render(self):  # Render board
        game_display.fill(white)  # Background
        if self.client_state == self.client_state_dict['OK']:
            self.apple.render(game_display)   # Render Apple
            self.snake.render(game_display, self.snake.get_number_body()-1)
            for key in self.enemy_dict:
                self.enemy_dict[key].render(game_display, self.enemy_dict[key].get_number_body()-1)
            self.hud.time_hud(game_display, self.game_time, width / 2, height * 0.05)
            self.hud.score_hud(game_display, self.snake.get_score(), width * 0.8, height * 0.05)
            self.hud.gauge_hud(game_display, min(self.snake.get_slide_ellapse() / self.snake.get_slide_delay(), 1), 0.6 * width, 0.95 * height, 0.4 * width, 0.01 * height)
            self.hud.gauge_hud(game_display, min(self.snake.get_run_use_ellapse() / self.snake.get_run_use_delay(), 1), 0.6 * width, 0.97 * height, 0.4 * width, 0.01 * height)
        pygame.display.update()  # Update display
        
    def loop(self):  # Loop to play always
        self.client = ClientManager("localhost", 8000)
        packet = str("tile:" + str(width) + "," + str(height) + "," +  str(self.nw_tile) + "," +  str(self.nh_tile))
        self.client.send(packet)
        self.client.close()
        while True :
            try:
                self.client = ClientManager("localhost", 8000)
                self.update()  # Update program
                self.render()  # Render program
                self.client.close()
            except KeyboardInterrupt :
                pygame.quit()  # Quit program
                quit()
        pygame.quit()  # Quit program
        quit()
    
width = 600
height = 600

white = (255 ,255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

framerate = 0

pygame.init()       # Start pygame
game_display = pygame.display.set_mode([width, height])  # Start Frame
pygame.display.set_caption("SNAKEGAME_2D")  # Set caption
clock = pygame.time.Clock()  # Set counter

board_mng = BoardManager(30, 30)  # Setup BoardManager
board_mng.loop()   # Loop BoardManager