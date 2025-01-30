from settings import *

class Music:
    def __init__(self):
        self.paused = False

    def play(self, music):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music)
        pygame.mixer.music.play()                                                                     # The '-1' means repeat endlessly

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

