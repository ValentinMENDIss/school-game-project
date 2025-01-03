######### IMPORT ##############

from settings import *

######### SPRITEs ##############

ITEM_TEST = pygame.image.load(os.path.join('..', 'graphics', 'item-test.png'))                                          # load sprite of the ITEM_TEST
ITEM_TEST2 = pygame.image.load(os.path.join('..', 'graphics', 'item-test2.png'))                                          # load sprite of the ITEM_TEST2

######### CLASSes ##############

class Items(pygame.sprite.Sprite):
    def __init__(self, pos, name, groups):
        super().__init__(groups)                                                                                        # this subclass sets up the basic properties and methods that it inherits from its parent class (group)

        if name == "test-image":
            self.image = ITEM_TEST.convert_alpha()
        elif name == "test-image2":
            self.image = ITEM_TEST2.convert_alpha()
        else:                                                                                                           # if something is wrong, say image name isn't detected, it will take the default image and not crash the whole game
            self.image = ITEM_TEST

        self.rect = self.image.get_frect(center=pos)                                                                    # convert image to rectangle (needed for collision in the future), center is position that was provided during construction (__init__())