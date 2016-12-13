import time

class CounterTime():
    
    def __init__(self):
        self.is_stop = True
        self.ellapse = 0

    def update(self):
        if not self.is_stop: 
          self.ellapse = time.time() - self.start
        else:
            self.ellapse = 0
    
    def restart(self):
        self.is_stop = False
        self.start = time.time()
        self.ellapse = 0
    
    def stop(self):
        self.is_stop = True
        self.ellapse = 0
    
    def get_time(self):
        return self.ellapse
    
    def compare(self, delay):
        if self.ellapse > delay:
            return True
        return False
    
    def get_stop(self):
        return self.is_stop