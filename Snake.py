import pygame
from Object import Object
from CounterTime import CounterTime

class Snake(Object) :
    
    def __init__(self, x, y, tile_mng, color, typ, _id, number_body):
        Object.__init__(self, x, y, tile_mng, color, typ)
        self._id = _id  # Set id of snake
        
        self.score = 0  # Set score of snake
        self.x_pos = [self.get_x() - (number_body - 1 - i) * self.get_width() for i in range(number_body)]  #Set all x postion
        self.y_pos = [self.get_y()] * number_body   # Set all y position
        self.dx = self.get_width()  # Set speed of x
        self.dy = 0     # Set speed of y
        self.move_list = {'left':False, 'right':False, 'up':False, 'down':False}    # Set move state list
        self.move = 'right'     # Move state
        self.state = 'move'     # State of snake
        
        self.walk_counter = CounterTime()  # Timer of walking
        self.snake_walk_delay = 0.06       # Walking delay
        self.walk_counter.restart()        # Walking's timer start
        
        self.slide_counter = CounterTime()  # Timer of slide skill
        self.slide_delay = 5                # Delay of slide skill
        self.slide_counter.restart()        # Timer of slide skill start
        
        self.running_counter = CounterTime()    # Timer of running skill
        self.running_delay = 1.5                # Running skill Delay
        
        self.run_use_counter = CounterTime()    # Timer of wait running again
        self.run_use_delay = 3                  # Delay of wait running again
        self.run_use_counter.restart()          # Start wait running timer
        
        self.dead_counter = CounterTime()       # Dead timer
        self.dead_delay = 3                     # Dead delay
        
        self.prepare_walk_counter = CounterTime()   # Prepare to walk counter
        self.prepare_walk_delay = 3                 # Prepare to walk delat
    
    def prepare_walk(self, number_body):    # Set x, y position and speed(stop) when prepare to walk
        self.x_pos = [self.get_x() - (number_body - 1 - i) * self.get_width() for i in range(number_body)]
        self.y_pos = [self.get_y()] * number_body
        self.dx = 0
        self.dy = 0

    def update(self) :  # Update snake
        if self.state == 'move' :   # Move state
            self.snake_collision(len(self.x_pos) - 1)   # Snake walk out from frame
            if self.running_counter.compare(self.running_delay) and self.run_use_counter.get_stop():    # Running skill time out
                self.snake_walk_delay = 0.06    # Set delay
                self.running_counter.stop()
                self.run_use_counter.restart()
            if self.walk_counter.compare(self.snake_walk_delay) :   # Walking timer timeout
                self.shift_body(len(self.x_pos) - 1)    # Shift body of snake
                self.walk_snake()       # Head of snake move
                self.walk_counter.restart()
                self.x = self.x_pos[-1]     # Set x and y pos
                self.y = self.y_pos[-1]
                self.snake_check_dead(len(self.x_pos)-2)    # Check snake is dead
            # Update timer
            self.walk_counter.update()  
            self.slide_counter.update()
            self.running_counter.update()
            self.run_use_counter.update()
        elif self.state == 'prepare':   # State is prepare
            self.prepare_walk_counter.update()  # Update 
            if self.prepare_walk_counter.compare(self.prepare_walk_delay):  # ready to walk
                self.state = 'move'         # State is move
                self.prepare_walk_counter.stop()
                self.dx = self.get_width()  # Speed to move to right
                self.dy = 0
                self.move = 'right'
                self.walk_counter.restart()
                self.slide_counter.restart()
                self.run_use_counter.restart()
        elif self.state == 'dead':  # State is dead
            self.dead_counter.update()  # Dead counter update
            self.walk_counter.stop()
            self.slide_counter.stop()
            self.running_counter.stop()
            self.run_use_counter.stop()
            if self.dead_counter.compare(self.dead_delay) : # Dead counter is time up => prepare to walk
                self.state = 'prepare'
                self.prepare_walk_counter.restart()
                self.dead_counter.stop()
                self.prepare_walk(3)
            
    
    def render(self, game_display, i) :
        if i < 0 : return
        if self.state == 'move' :   # Draw snake
            pygame.draw.rect(game_display, self.color, [int(self.x_pos[len(self.x_pos)-1-i]), \
                                                        int(self.y_pos[len(self.y_pos)-1-i]), \
                                                        int(self.get_width()), int(self.get_height())])
        elif self.state == 'prepare':
            if self.prepare_walk_counter.get_time() * 200 % 200 >= 100 :    # Draw blink snake
                pygame.draw.rect(game_display, self.color, [int(self.x_pos[len(self.x_pos)-1-i]), \
                                                        int(self.y_pos[len(self.y_pos)-1-i]), \
                                                        int(self.get_width()), int(self.get_height())])
        self.render(game_display, i-1)
                
    def snake_collision (self, i):  # Snake is out from frame
        if i < 0 :
            return
        if self.x_pos[i] < 0 :  # Out from right => left
            self.x_pos[i] = self.tile_mng.get_wframe() - self.get_width()
        elif self.x_pos[i] >= self.tile_mng.get_wframe():   # Out from left => right
            self.x_pos[i] = 0
        if self.y_pos[i] < 0 :  # Out from above => below
            self.y_pos[i] = self.tile_mng.get_hframe() - self.get_height()
        elif self.y_pos[i] >= self.tile_mng.get_hframe():   # Out from below => above
            self.y_pos[i] = 0
    
    def shift_body(self, i):    # Move body of snake
        if i < 1 :
            return
        self.x_pos[len(self.x_pos)-i-1] = self.x_pos[len(self.x_pos)-i]
        self.y_pos[len(self.y_pos)-i-1] = self.y_pos[len(self.y_pos)-i]
        self.shift_body(i-1)
        
    def walk_snake(self):   # Set head of snake 
        self.x_pos[len(self.x_pos)-1] += self.dx
        self.y_pos[len(self.y_pos)-1] += self.dy
        
    def snake_eat_apple(self, apple):   # Check apple is eaten
        if (self.x_pos[-1] <= apple.get_x() and
            self.x_pos[-1] + self.get_width() >= apple.get_x() + apple.get_width() and
            self.y_pos[-1] <= apple.get_y() and
            self.y_pos[-1] + self.get_height() >= apple.get_y() + apple.get_height()) : # Head of snake touch apple
                apple.set_eaten(True)   # Set apple is eaten is true
                x_pos2 = list(self.x_pos[:])  # Add head of snake
                y_pos2 = list(self.y_pos[:])
                self.x_pos.append(x_pos2[-1])
                self.y_pos.append(y_pos2[-1])
                self.score += 1     # Add score
    
    # Snake shift to near apple
    def snake_slide(self, code, apple):
        if self.slide_counter.compare(self.slide_delay) : 
            if code == 'left' or code == 'right' :  # Snake go left or right
                if self.y < apple.get_y():  # apple is below of snake => move down
                    self.y_pos = [self.y_pos[i] + self.get_height() for i in range(self.get_number_body())]
                elif self.y > apple.get_y():    # apple is above of snake => move up
                    self.y_pos = [self.y_pos[i] - self.get_height() for i in range(self.get_number_body())]
            elif code == 'up' or code == 'down' :   # Snake go up or down
                if self.x < apple.get_x():  # apple is right of snake => move right
                    self.x_pos = [self.x_pos[i] + self.get_width() for i in range(self.get_number_body())]
                elif self.x > apple.get_x():     # apple is left of snake => move left
                    self.x_pos = [self.x_pos[i] - self.get_width() for i in range(self.get_number_body())]
            self.slide_counter.restart()    # Start to Slide
    
    # Snake begin to run
    def snake_running(self):
        if self.run_use_counter.compare(self.run_use_delay) and self.running_counter.get_stop():
            self.snake_walk_delay = 0
            self.run_use_counter.stop()
            self.running_counter.restart()
    
    # Head snake touch body snake = dead
    def snake_check_dead(self, index):
        if index < 0 : return
        if self.x_pos[-1] == self.x_pos[index] and self.y_pos[-1] == self.y_pos[index]:
            self.state = 'dead'
            self.dead_counter.restart()
            return
        self.snake_check_dead(index-1)
        
            
    def get_id(self):
        return self._id
    
    def get_number_body(self):
        return len(self.x_pos)
    
    def get_move_list(self, index):
        return self.move_list[index]
    
    def get_x_pos(self):
        return self.x_pos
    
    def get_y_pos(self):
        return self.y_pos
    
    def get_score(self):
        return self.score
    
    def get_move(self):
        return self.move
    
    def get_slide_ellapse(self):
        return self.slide_counter.get_time()
    
    def get_slide_delay(self):
        return self.slide_delay
    
    def get_run_use_ellapse(self):
        return self.run_use_counter.get_time()
    
    def get_run_use_delay(self):
        return self.run_use_delay
    
    def get_dead_ellapse(self):
        return self.dead_counter.get_time()
    
    def get_dead_delay(self):
        return self.dead_delay
    
    def get_state(self):
        return self.state
    
    def set_score(self):
        self.score = score
    
    def set_pos(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
    
    def set_left(self):
        self.move = 'left'
        self.dx = -self.get_width()
        self.dy = 0
        self.move_list['left'] = True
        self.move_list['right'] = False
        self.move_list['up'] = False
        self.move_list['down'] = False
        
    def set_right(self):
        self.move = 'right'
        self.dx = self.get_width()
        self.dy = 0
        self.move_list['right'] = True
        self.move_list['left'] = False
        self.move_list['up'] = False
        self.move_list['down'] = False
        
    def set_up(self):
        self.move = 'up'
        self.dx = 0
        self.dy = -self.get_height()
        self.move_list['up'] = True
        self.move_list['left'] = False
        self.move_list['right'] = False
        self.move_list['down'] = False
        
    def set_down(self):
        self.move = 'down'
        self.dx = 0
        self.dy = self.get_height()
        self.move_list['down'] = True
        self.move_list['left'] = False
        self.move_list['right'] = False
        self.move_list['up'] = False