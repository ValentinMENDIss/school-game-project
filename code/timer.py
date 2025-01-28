from pygame.time import get_ticks

class Timer:
    def __init__(self):
        self.start_time = 0
        self.active = False
        self.is_finished = False

    def start(self, duration_time):
        self.duration_time = duration_time
        self.start_time = get_ticks()
        self.active = True

    def stop(self):
        self.active = False
        self.start_time = 0
        self.finished()

    def finished(self):
        self.is_finished = True

    def update(self):
        if self.active:
            current_time = get_ticks()
            if current_time - self.start_time >= self.duration_time:
                self.stop()
