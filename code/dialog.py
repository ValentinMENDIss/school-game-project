######### IMPORT ##############
from settings import *
from entities import *
from timer import Timer

######### CLASSES ##############

class Dialog:
    def __init__(self, npc_pos, game):
        #self.SCREEN = pygame.display.get_surface()                                                                      # initializing screen (SCREEN)
        self.pos = npc_pos                                                                                              # set npc's position to a variable 'pos'
        self.game = game

    def interact(self, text, player_center, screen):
        font = pygame.font.Font(os.path.join('..', 'font', 'Pixeltype.ttf'),20)                               # set Font and Size for the Small Text
        smalltext = font.render(text, True,(0, 0, 0)).convert_alpha()                                 # render a Small Text
        smalltextrect = smalltext.get_rect()                                                                            # get a Rectangle of the small Text ( needed, to be able to place the Text precisely )

        self.offset_x = - ((player_center[0] - WINDOW_WIDTH / 2) + 25)                                                  # offset x coordinates which are needed for camera (drawn near the npc even when the camera moves)
        self.offset_y = - ((player_center[1] - WINDOW_HEIGHT / 2) + 100)                                                # offset y coordinates which are needed for camera (drawn near the npc even when the camera moves)

        smalltextrect.topleft = (self.pos[0] + self.offset_x, self.pos[1] + self.offset_y)                              # place a text near to the npc's coordinates + offset (needed for camera effect)

        screen.blit(smalltext, smalltextrect)

    def interactInRange(self, text, player_center, screen):
        font = pygame.font.Font(os.path.join('..', 'font', 'DepartureMonoNerdFont-Regular.otf'), 18)                     # set Font and Size for the Small Text
        smalltext = font.render(text, True,(0, 0, 0)).convert_alpha()                                                   # render a Small Text
        smalltextrect = smalltext.get_rect()                                                                            # get a Rectangle of the small Text ( needed, to be able to place the Text precisely )

        self.offset_x = - ((player_center[0] - WINDOW_WIDTH / 2) + 65)                                                  # offset x coordinates which are needed for camera (drawn near the npc even when the camera moves)
        self.offset_y = - ((player_center[1] - WINDOW_HEIGHT / 2) + 135)                                                # offset y coordinates which are needed for camera (drawn near the npc even when the camera moves)

        smalltextrect.center = (self.pos[0] + self.offset_x, self.pos[1] + self.offset_y)                              # place a text near to the npc's coordinates + offset (needed for camera effect)

        screen.blit(smalltext, smalltextrect)

    def interactDialog(self, text_data, screen):
        timer = Timer()
        x = 0
        while x < len(text_data):
            text = text_data[x]
            x += 1
            font = pygame.font.Font(os.path.join('..', 'font', 'DepartureMonoNerdFont-Regular.otf'), 18)
            smalltext = font.render(text, True,(0, 0, 0)).convert_alpha()                                                   # render a Small Text
            smalltextrect = smalltext.get_rect()                                                                            # get a Rectangle of the small Text ( needed, to be able to place the Text precisely )
        
            smalltextrect.topleft = (WINDOW_WIDTH // 2 - 300, WINDOW_HEIGHT - 275)
            offset_y = -15
            pygame.draw.rect(screen, (255, 255, 255), (WINDOW_WIDTH // 2 - 325, WINDOW_HEIGHT - 300 + offset_y, 650, 300))
            screen.blit(smalltext, smalltextrect)
            pygame.display.update()
            timer.start(3000, loop=True)                                                       # set timer for 'n' ms
            while timer.is_finished == False:
                timer.update()                                                              # update timer's state
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key ==  pygame.K_e:
                            timer.is_finished = True
 