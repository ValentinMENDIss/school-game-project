######### IMPORT ##############
from settings import *
from entities import *

######### CLASSES ##############

class Dialog:
    def __init__(self):
        self.SCREEN = pygame.display.get_surface()  # initializing screen (SCREEN)

    def interact(self,text):
        smalltext = pygame.font.Font(os.path.join('..', 'font', 'Pixeltype.ttf'),20)  # Set Font and Size for the Small Text
        smalltext = smalltext.render(text, True,(0, 0, 0)).convert_alpha()  # Render a Small Text
        smalltextrect = smalltext.get_rect()  # Get a Rectangle of the small Text ( needed, to be able to place the Text precisely )
        smalltextrect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30)  # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )

        self.SCREEN.blit(smalltext, smalltextrect)  # Draw a Text on the Screen