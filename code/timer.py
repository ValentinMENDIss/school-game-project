from pygame.time import get_ticks

class Timer:
    def __init__(self, duration_time):
        self.start_time = 0
        self.duration_time = duration_time
        self.active = False
        self.start()

    def start(self):
        self.start_time = get_ticks()
        self.active = True
       
    def stop(self):
        self.active = False 
        self.start_time = 0

    def update(self):
        if self.active:
            current_time = get_ticks()
            if current_time - self.start_time >= self.duration_time:
                self.stop()
 
