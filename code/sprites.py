######### IMPORT ##############

from settings import *


######### CLASSes #############

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)                        # use the original group's instructions to set up the new class (Sprite)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos) # get_frect = get float rectangle position (better precision)