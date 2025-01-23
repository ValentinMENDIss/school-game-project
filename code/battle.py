######### IMPORT ##############

import pygame

from settings import *

######### SPRITES ##############

BACKGROUND_IMG = pygame.image.load(os.path.join('..', 'graphics', 'background.png'))

######### CLASSes ##############

class Battle_Menu:
    def __init__(self):
        self.text = ""
        self.running = True
        self.get_pressed_keys_action = False
        self.menu_exit_action = False

    def get_input(self):
        pass

    # DRAWING LOGIC
    def show(self, surface):
        self.running = True
        self.exit_action = False
        while self.running:
            self.draw(surface)
            if self.exit_action:
                self.running = False

    def draw(self, surface):
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

        ## EVENTS ##
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                                                                               # exit game function
                self.running = False

        pygame.display.update()
    

        




