######### IMPORT ##############

from settings import *
from entities import Player, NPC

######### CLASSes ##############
class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()                                                                                              # inherit all the functionality and attributes of the pygame.sprite.Group class
        self.SCREEN = pygame.display.get_surface()                                                                      # initializing screen (SCREEN)
        self.offset = vector()                                                                                          # creating offset for camera

    def draw(self, player_center):                                                                                      # drawing method for camera
        self.offset.x = -(player_center[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(player_center[1] - WINDOW_HEIGHT / 2)

        # LAYERS (SORTING CLASSES IN LAYERS)
        bg_sprites = [sprite for sprite in self if sprite.z < WORLD_LAYERS['main']]
        main_sprites = sorted([sprite for sprite in self if sprite.z == WORLD_LAYERS['main']], key=lambda sprite: sprite.y_sort) # lambda = quick, one-time function  #creating a sorting key function that extracts the y_sort attribute from each sprite object. Allows the sprites to be sorted based on their y_sort value. Used to determine their vertical drawing order
        fg_sprites = [sprite for sprite in self if sprite.z > WORLD_LAYERS['main']]

        for layer in (bg_sprites, main_sprites, fg_sprites):                                                                # return all sprites that are in this class (AllSprites) and in these layers
            for sprite in layer:
                if isinstance(sprite, Player or NPC):
                    self.SCREEN.blit(sprite.image, sprite.rect.topleft + self.offset)
                self.SCREEN.blit(sprite.image, sprite.rect.topleft + self.offset)
