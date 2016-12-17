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
    
    def  __init__(self, nw_tile, nh_tile):
        self.nw_tile = nw_tile  # Set number of tile in x
        self.nh_tile = nh_tile  # Set number of tile in y
        
        self.number_body = 3    # Set number of snake's body
        self.score = 0          # Set score of sanke
        
        self.db_save_size = 6   # Column size of data base
        self.id = 0             # index of database's column
        self.type = 1           
        self.x = 2
        self.y = 3
        self.s = 4
        self.t = 5
        
        self.enemy_dict = {}     # Enemy snake dictionary
        self.client_state_dict = {'OK':0, 'notNStart':1, 'notNExit':2}  # KList state of client
        self.client_state = self.client_state_dict['notNStart']         # State of cleint 
        self.play_state = False     # Playing state
        self.game_time = 0          # time of game
        
        self.tile_mng = TileManager(width, height, self.nw_tile, self.nh_tile)  # Set TileManager
        self.snake = Snake(1, 1, self.tile_mng, green, SNAKE, raw_input("Enter : "), self.number_body)  # Set my sanke
        self.apple = Apple(0, 0, self.tile_mng, red, 0)     # Set apple
        self.hud = HUD()        # Set HUD
        
    # Update board
    def update(self):
        for event in pygame.event.get():  # Check all event
            if event.type == pygame.QUIT:  # Click Quit to quit program
                pygame.quit()   # quit programe
                quit()
            if event.type == pygame.KEYDOWN :   # If pressed keyboard
                if event.key == pygame.K_LEFT and not self.snake.get_move_list('right'):   # Pressed left and not go right
                    self.snake.set_left()       # Go left
                elif event.key == pygame.K_RIGHT and not self.snake.get_move_list('left'): # Pressed right and not go left
                    self.snake.set_right()      # Go right
                elif event.key == pygame.K_UP and not self.snake.get_move_list('down'):     # Pressed up and not go down
                    self.snake.set_up()         # Go up
                elif event.key == pygame.K_DOWN and not self.snake.get_move_list('up'):     # Pressed down and not go up
                    self.snake.set_down()       # Go down
                elif event.key == pygame.K_x:   # Press x
                    self.snake.snake_slide(self.snake.get_move(), self.apple)   # Use slide snake skill
                elif event.key == pygame.K_c:   # Press c
                    self.snake.snake_running()  # Use running snake skill
            
        x_pos_ls = [int(self.snake.get_x_pos()[i] / self.tile_mng.get_sizew_tile()) for i in range(self.snake.get_number_body())]   # set x's list
        y_pos_ls = [int(self.snake.get_y_pos()[i] / self.tile_mng.get_sizeh_tile ())for i in range(self.snake.get_number_body())]   # set y's list
        x_pos_n = self.client.pos_pattern(x_pos_ls)     # save in string in postion pattern (x, y)
        y_pos_n = self.client.pos_pattern(y_pos_ls)
        pattern = self.client.set_pattern(self.snake.get_id(), [self.snake.get_type(), x_pos_n, y_pos_n, self.snake.get_score(), 0]) # set pattern of all data
        # id,type,xs,ys,score,time
        
        if self.client_state == self.client_state_dict['OK']: # Client state is "OK"
            self.snake.snake_eat_apple(self.apple)  # Check does snake eat apple ?
            self.snake.update() # Update snake
            if self.apple.get_eaten():  # Apple is eaten by snake
                pattern = "eaten"   # pattern is "eaten"
                self.apple.set_eaten(False)     # Apple is not eaten
        self.client.send(pattern)   # Send pattern to client
        
        data, addr = self.client.recv()     # Receive data from server
        if data == None:    # Data is none => exit method
            return
        if data == "notNStart" :    # data is notNStart => set client state
            self.client_state = self.client_state_dict['notNStart']
        elif data == "notNExit" :   # data is notNExit => set client state
            self.client_state = self.client_state_dict['notNExit']
        else :  # otherwise
            self.client_state = self.client_state_dict['OK']    # Set client state to "OK"
            split_list = self.client.split(data)        # Split data
            for ls in split_list :
                self.game_time = int(ls[self.t])        # set time
                if ls[self.id] == "*" :    # See id of apple
                    self.apple = Apple(int(ls[self.x]), int(ls[self.y]), self.tile_mng, red, str(ls[self.type]))
                elif ls[self.id] != self.snake.get_id() and ls[self.id] != "*":  # See enemy snake's id
                    self.enemy_dict[ls[self.id]] = Snake(0, 0, self.tile_mng, blue, ls[self.type], ls[self.id], 0)  # Save in dictionary of enemy snake
                    x_pos = self.client.pos_split(ls[self.x]) 
                    y_pos = self.client.pos_split(ls[self.y])
                    x_list = [int(x_pos[i] * self.tile_mng.get_sizew_tile()) for i in range(len(x_pos))]
                    y_list = [int(y_pos[i] * self.tile_mng.get_sizeh_tile()) for i in range(len(y_pos))]
                    self.enemy_dict[ls[self.id]].set_pos(x_list, y_list)    # Set postion enemy snake
         
    # Render board
    def render(self):  # Render board
        game_display.fill(white)  # Background
        if self.client_state == self.client_state_dict['OK']:   # Client state is OK
            if self.snake.state == 'dead' : # If dead
                # Draw dead HUD
                self.hud.dead_hud(game_display, self.snake.get_dead_ellapse(), self.snake.get_dead_delay(), width / 2, height / 2, width / 3, height / 3) 
            else :
                self.apple.render(game_display)   # Render Apple
                self.snake.render(game_display, self.snake.get_number_body()-1) # render snake
                for key in self.enemy_dict: # Render enemy snake
                    self.enemy_dict[key].render(game_display, self.enemy_dict[key].get_number_body()-1)
                # Draw time's hud, score' hud, gauge's hud
                self.hud.time_hud(game_display, self.game_time, width / 2, height * 0.05)
                self.hud.score_hud(game_display, self.snake.get_score(), width * 0.8, height * 0.05)
                self.hud.gauge_hud(game_display, min(self.snake.get_slide_ellapse() / self.snake.get_slide_delay(), 1), 0.6 * width, 0.95 * height, 0.4 * width, 0.02 * height)
                self.hud.gauge_hud(game_display, min(self.snake.get_run_use_ellapse() / self.snake.get_run_use_delay(), 1), 0.6 * width, 0.97 * height, 0.4 * width, 0.02 * height)
        pygame.display.update()  # Update display
        
    def loop(self):  # Loop to play always
        self.ip = raw_input("IP : ")    # Get IP
        self.client = ClientManager(self.ip, 8000)  # Set client 
        packet = str("tile:" + str(width) + "," + str(height) + "," +  str(self.nw_tile) + "," +  str(self.nh_tile))    # Set pattern : width, height program and number of tile program
        self.client.send(packet)    # Send data to server
        self.client.close()         # Disconnnet socket
        while True :
            try:
                self.client = ClientManager(self.ip, 8000)  # Set client
                self.update()  # Update program
                self.render()  # Render program
                self.client.close() # Disconnect from socket
            except KeyboardInterrupt :
                pygame.quit()  # Quit program
                quit()
        pygame.quit()  # Quit program
        quit()
    
width = 600     # width of program
height = 600    # height of program

white = (255 ,255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

pygame.init()       # Start pygame
game_display = pygame.display.set_mode([width, height])  # Start Frame
pygame.display.set_caption("SNAKEGAME_2D")  # Set caption
clock = pygame.time.Clock()  # Set counter

board_mng = BoardManager(8, 8)  # Setup BoardManager
board_mng.loop()   # Loop BoardManager