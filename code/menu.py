######### IMPORT ##############
from settings import *


######### CLASSES #############
class Menu:
    def __init__(self):
        self.text = ""


    def draw(self, surface):
        # SETTING TEXT FOR MENU
        self.small_text = "Press ESC to proceed"
        self.big_text = "Menu"

        # DEFINING TEXT VARIABLES
        smalltext = pygame.font.Font(os.path.join('..', 'font', 'Pixeltype.ttf'),25)  # set Font and Size for the Small Text
        smalltext = smalltext.render(self.small_text, True, (0, 0, 0)).convert_alpha()  # render a Small Text
        smalltextrect = smalltext.get_rect()  # get a Rectangle of the small Text ( needed, to be able to place the Text precisely )
        smalltextrect.center = (WINDOW_WIDTH // 2, + WINDOW_HEIGHT // 2)                                                                           # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )

        bigtext = pygame.font.Font(os.path.join('..', 'font', 'Pixeltype.ttf'),65)  # set Font and Size for the Small Text
        bigtext = bigtext.render(self.big_text, True, (0, 0, 0)).convert_alpha()  # render a Small Text
        bigtextrect = bigtext.get_rect()  # get a Rectangle of the small Text ( needed, to be able to place the Text precisely )
        bigtextrect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 250)                                                                           # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )



        # DRAWING TO SURFACE
        surface.fill((255, 255, 255))  # Draw a White coloured Screen
        surface.blit(smalltext, smalltextrect)                                                                                       # Draw a Text on the Screen
        surface.blit(bigtext, bigtextrect)
        pygame.display.update()

    def show(self, surface):
        self.running = True
        while self.running:
            self.draw(surface)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False