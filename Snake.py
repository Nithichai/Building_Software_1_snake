import pygame
from Object import Object
from CounterTime import CounterTime

class Snake(Object) :
    
    def __init__(self, x, y, tile_mng, color, typ, _id, number_body):
        Object.__init__(self, x, y, tile_mng, color, typ)
        self._id = _id
        
        self.score = 0
        self.x_pos = [self.get_x() - (number_body - 1 - i) * self.get_width() for i in range(number_body)]
        self.y_pos = [self.get_y()] * number_body
        self.dx = self.get_width()
        self.dy = 0
        self.move_list = {'left':False, 'right':False, 'up':False, 'down':False}
        self.move = 'right'
        self.state = 'move'
        
        self.walk_counter = CounterTime()
        self.snake_walk_delay = 0.06
        self.walk_counter.restart()
        
        self.slide_counter = CounterTime()
        self.slide_delay = 5
        self.slide_counter.restart()
        
        self.running_counter = CounterTime()
        self.running_delay = 1.5
        
        self.run_use_counter = CounterTime()
        self.run_use_delay = 3
        self.run_use_counter.restart()
        
        self.dead_counter = CounterTime()
        self.dead_delay = 10
        
        self.blink_counter = CounterTime()
        self.blink_delay = 3

    def update(self) :
        self.snake_collision(len(self.x_pos) - 1)
        if self.dead_counter.compare(self.dead_delay) :
            self.state = 'move'
            self.dead_counter.stop()
            self.blink_counter.restart()
        if self.running_counter.compare(self.running_delay) and self.run_use_counter.get_stop():
            self.snake_walk_delay = 0.06
            self.running_counter.stop()
            self.run_use_counter.restart()
        if self.walk_counter.compare(self.snake_walk_delay) :
            self.shift_body(len(self.x_pos) - 1)
            self.walk_snake()
            self.walk_counter.restart()
            self.x = self.x_pos[-1]
            self.y = self.y_pos[-1]
        self.walk_counter.update()
        self.slide_counter.update()
        self.running_counter.update()
        self.run_use_counter.update()
        self.dead_counter.update()
        
    
    def render(self, game_display, i) :
        if i < 0 :
            return
        pygame.draw.rect(game_display, self.color, [int(self.x_pos[len(self.x_pos)-1-i]), \
                                                    int(self.y_pos[len(self.y_pos)-1-i]), \
                                                    int(self.get_width()), int(self.get_height())])
        self.render(game_display, i-1)
                
    def snake_collision (self, i):
        if i < 0 :
            return
        if self.x_pos[i] < 0 :
            self.x_pos[i] = self.tile_mng.get_wframe() - self.get_width()
        elif self.x_pos[i] >= self.tile_mng.get_wframe():
            self.x_pos[i] = 0
        elif self.y_pos[i] < 0 :
            self.y_pos[i] = self.tile_mng.get_hframe() - self.get_height()
        elif self.y_pos[i] >= self.tile_mng.get_hframe():
            self.y_pos[i] = 0
    
    def shift_body(self, i):
        if i < 1 :
            return
        self.x_pos[len(self.x_pos)-i-1] = self.x_pos[len(self.x_pos)-i]
        self.y_pos[len(self.y_pos)-i-1] = self.y_pos[len(self.y_pos)-i]
        self.shift_body(i-1)
        
    def walk_snake(self):
        self.x_pos[len(self.x_pos)-1] += self.dx
        self.y_pos[len(self.y_pos)-1] += self.dy
        
    def snake_eat_apple(self, apple):
        if (self.x_pos[-1] <= apple.get_x() and
            self.x_pos[-1] + self.get_width() >= apple.get_x() + apple.get_width() and
            self.y_pos[-1] <= apple.get_y() and
            self.y_pos[-1] + self.get_height() >= apple.get_y() + apple.get_height()) :
                apple.set_eaten(True)
                x_pos2 = list(self.x_pos[:])
                y_pos2 = list(self.y_pos[:])
                self.x_pos.append(x_pos2[-1])
                self.y_pos.append(y_pos2[-1])
                self.score += 1
    
    def snake_slide(self, code, apple):
        if self.slide_counter.compare(self.slide_delay) : 
            if code == 'left' or code == 'right' :
                if self.y < apple.get_y():
                    self.y_pos = [self.y_pos[i] + self.get_height() for i in range(self.get_number_body())]
                elif self.y > apple.get_y():
                    self.y_pos = [self.y_pos[i] - self.get_height() for i in range(self.get_number_body())]
            elif code == 'up' or code == 'down' :
                if self.x < apple.get_x():
                    self.x_pos = [self.x_pos[i] + self.get_width() for i in range(self.get_number_body())]
                elif self.x > apple.get_x():
                    self.x_pos = [self.x_pos[i] - self.get_width() for i in range(self.get_number_body())]
            self.slide_counter.restart()
    
    def snake_running(self):
        if self.run_use_counter.compare(self.run_use_delay) and self.running_counter.get_stop():
            self.snake_walk_delay = 0
            self.run_use_counter.stop()
            self.running_counter.restart()
                
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