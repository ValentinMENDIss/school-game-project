######### IMPORT ##############

from settings import *


######### CLASSes #############

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = WORLD_LAYERS['main']):
        super().__init__(groups)                        # use the original group's instructions to set up the new class (Sprite)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos) # get_frect = get float rectangle position (better precision)
        self.z = z
        self.y_sort = self.rect.centery

class BorderSprite(Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)             # parse in (pos, surf, groups) from Sprite()'s constructor
        self.hitbox = self.rect.copy()                  # initialize new variable that stores rect. position of BorderSprite()'s Object

