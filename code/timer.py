from pygame.time import get_ticks

class Timer:
    def __init__(self):
        self.start_time = 0
        self.active = False
        self.is_finished = False

    def start(self, duration_time, loop=False):
        self.duration_time = duration_time
        self.start_time = get_ticks()
        self.active = True
        if loop:
            self.is_finished = False

    def stop(self, loop=False):
        self.active = False
        self.start_time = 0
        if loop == False:
            self.finished()
        else:
            self.not_finished()
    
    def not_finished(self):
        self.is_finished = False

    def finished(self):
        self.is_finished = True

    def update(self):
        if self.active:
            current_time = get_ticks()
            if current_time - self.start_time >= self.duration_time:
                self.stop()
