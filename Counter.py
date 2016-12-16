class Counter():
    
    def __init__(self, framerate, delay):
        self.frame = 0
        self.framerate = framerate
        self.is_stop = False
        self.delay = self.framerate * delay
    
    def start(self):
        self.frame = 0
        self.is_stop = False
    
    def update(self):
        if not self.is_stop:
            self.frame += 1
    
    def compare(self):
        if self.frame > self.delay and not self.is_stop:
            self.start()
            return True
        return False
    
    def set_delay(self, value):
        self.delay = self.framerate * value
    
    def stop(self):
        self.is_stop = True
    
    def continues(self):
        self.is_stop = False
    
    def get_time(self):
        return int(self.frame / self.framerate)
    
    def get_delay(self):
        return self.delay
