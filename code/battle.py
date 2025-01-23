######### IMPORT ##############

import pygame

from settings import *
from button import Button

######### SPRITES ##############

BACKGROUND_IMG = pygame.image.load(os.path.join('..', 'graphics', 'battle-menu-background.png'))

######### CLASSes ##############

class Battle_Menu:
    def __init__(self):
        self.text = ""
        self.get_pressed_keys_action = False
        self.exit_action = False

    def get_input(self):
        pass

    # DRAWING LOGIC
    def draw(self, surface):
        running = True
        while running:
            # DEFINING CONSTANT VARIABLES
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            # SETTING TEXT FOR MENU
            heading_text = "Battle Menu"

            # DEFINING TEXT VARIABLES
            headingtext = HEADINGTEXT.render(heading_text, True, (0, 0, 0)).convert_alpha()  # render a Small Text
            headingtextrect = headingtext.get_rect()                                                              # get a Rectangle of the small Text ( needed, to be able to place the text precisely )
            headingtextrect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 250)                                     # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )

            # DRAWING ON THE SURFACE
            surface.blit(BACKGROUND_IMG)
            surface.blit(headingtext, headingtextrect)

            ## INITIALIZING BUTTONS AND DRAWING THEM ##
            SURRENDER_BUTTON = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100, START_IMG, 0.5) # create button instance
            SURRENDER_BUTTON.draw(surface)

            ## EVENTS ##
            for event in pygame.event.get():
                if event.type == pygame.QUIT:                                                                               # exit game function
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if SURRENDER_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.mixer.Sound.play(MENU_SOUND)
                        pygame.mixer.music.stop()
                        running = False

            pygame.display.update()
            
