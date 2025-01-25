######### IMPORT ##############
from settings import *
from entities import *

######### CLASSES ##############

class Dialog:
    def __init__(self, npc_pos):
        #self.SCREEN = pygame.display.get_surface()                                                                      # initializing screen (SCREEN)
        self.pos = npc_pos                                                                                              # set npc's position to a variable 'pos'

    def interact(self, text, player_center, screen):
        smalltext = pygame.font.Font(os.path.join('..', 'font', 'Pixeltype.ttf'),20)                               # set Font and Size for the Small Text
        smalltext = smalltext.render(text, True,(0, 0, 0)).convert_alpha()                                 # render a Small Text
        smalltextrect = smalltext.get_rect()                                                                            # get a Rectangle of the small Text ( needed, to be able to place the Text precisely )

        self.offset_x = - ((player_center[0] - WINDOW_WIDTH / 2) + 25)                                                  # offset x coordinates which are needed for camera (drawn near the npc even when the camera moves)
        self.offset_y = - ((player_center[1] - WINDOW_HEIGHT / 2) + 100)                                                # offset y coordinates which are needed for camera (drawn near the npc even when the camera moves)

        smalltextrect.topleft = (self.pos[0] + self.offset_x, self.pos[1] + self.offset_y)                              # place a text near to the npc's coordinates + offset (needed for camera effect)

        #self.SCREEN.blit(smalltext, smalltextrect)                                                                      # draw a text with its coordinates
        screen.blit(smalltext, smalltextrect)
