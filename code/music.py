from settings import *

class Music:
    def __init__(self):
        self.paused = False
        pygame.mixer.music.set_volume(0.35)
    def play(self, music):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music)
        pygame.mixer.music.play()                                                                     # The '-1' means repeat endlessly

    def play_random(self):
        pygame.mixer.music.stop()
        index = random.randint(0, len(MUSIC) - 1)
        pygame.mixer.music.load(MUSIC[index])
        pygame.mixer.music.play()

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
