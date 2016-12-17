import time

class CounterTime():
    
    def __init__(self):     # Set timer
        self.is_stop = True
        self.ellapse = 0

    def update(self):       # Update timer
        if not self.is_stop: 
          self.ellapse = time.time() - self.start   # not stop => update value
        else:
            self.ellapse = 0    # stop => ellapse is zero
    
    def restart(self):      # Restart timer
        self.is_stop = False
        self.start = time.time()    # Set start time
        self.ellapse = 0
    
    def stop(self):         # Stop timer
        self.is_stop = True
        self.ellapse = 0
    
    def get_time(self):     # Get ellapse time
        return self.ellapse
    
    def compare(self, delay):   # If ellapse time more than dealy
        if self.ellapse > delay:
            return True
        return False
    
    def get_stop(self):     # Stop timer
        return self.is_stop