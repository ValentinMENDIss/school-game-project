from settings import *
from timer import Timer

class Music:
    def __init__(self):
        self.timer = Timer()
        self.paused = False
        self.fade = 5000                                                                                # music's fade-in/fade-out (in ms)
        self.volume = 0.35
        pygame.mixer.music.set_volume(self.volume)

    def play(self, music):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music)
        pygame.mixer.music.play()                                                                     # The '-1' means repeat endlessly

    def play_random(self):
        if self.timer.active == False and not self.timer.is_finished:
            self.timer.start(self.fade)
        if self.timer.is_finished:
            self.timer.is_finished = False
            pygame.mixer.music.stop()
            index = random.randint(0, len(MUSIC) - 1)
            pygame.mixer.music.load(MUSIC[index])
            pygame.mixer.music.play()
        self.timer.update()

    def check_status(self):
        if pygame.mixer.music.get_busy():
            return "Playing"
        else:
            if self.paused:
                return "Paused"
            elif self.paused == False:
                return "Stopped"

    def pause(self):
        pygame.mixer.music.pause()
        self.paused = True

    def unpause(self):
        pygame.mixer.music.unpause()
        self.paused = False

    def set_volume(self, volume):
        self.volume = volume
        pygame.mixer.music.set_volume(volume)

