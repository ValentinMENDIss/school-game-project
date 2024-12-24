from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()                                                                                              # inherit all the functionality and attributes of the pygame.sprite.Group class
        self.SCREEN = pygame.display.get_surface()                                                                      # initializing screen (SCREEN)
        self.offset = vector()                                                                                          # creating offset for camera

    def draw(self, player_center):                                                                                      # drawing method for camera
        self.offset.x = -(player_center[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(player_center[1] - WINDOW_HEIGHT / 2)

        for sprite in self:                                                                                             # return all sprites that are in this class (AllSprites)
            self.SCREEN.blit(sprite.image, sprite.rect.topleft + self.offset)                                           # draw every single sprite that is assigned to AllSprites() Class