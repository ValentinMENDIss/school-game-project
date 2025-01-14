######### IMPORT ##############
from settings import *
from button import *
from input import *

# LOADING IMAGES
BACKGROUND_IMG = pygame.image.load(os.path.join('..', 'graphics', 'background.png'))		                                # load image and use it as a menu background

######### CLASSES #############
class Menu:
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.text = ""
        self.running = True
        self.get_pressed_keys_action = False       
        self.menu_exit_action = False

    def show(self, surface):
        self.running = True
        self.exit_action = False
        while self.running:
            self.main_menu(surface)
            if self.exit_action:
                self.running = False

    def get_input(self):
        self.input = self.game.input
        self.input.menu()
        if self.input.menu_running == False:
            self.menu_exit_action = True
        else:
            self.menu_exit_action = False
 
    # GET PRESSED KEYS
    def get_pressed_keys(self, action):
        if self.get_pressed_keys_action:
            self.game.menu_get_pressed_keys(action)
            if self.game.menu_get_pressed_keys(action) == False:
                self.get_pressed_keys_action = False

    def main_menu(self, surface):
        running = True
        while running:
            # DEFINING CONSTANT VARIABLES
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            # SETTING TEXT FOR MENU
            heading_text = "Menu"

            # DEFINING TEXT VARIABLES
            headingtext = HEADINGTEXT.render(heading_text, True, (0, 0, 0)).convert_alpha()  # render a Small Text
            headingtextrect = headingtext.get_rect()                                                              # get a Rectangle of the small Text ( needed, to be able to place the text precisely )
            headingtextrect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 250)                                     # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )

            # DRAWING ON THE SURFACE
            surface.blit(BACKGROUND_IMG)
            surface.blit(headingtext, headingtextrect)

            ## INITIALIZING BUTTONS AND DRAWING THEM ##
            START_BUTTON = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, START_IMG, 0.8)  # create button instance
            START_BUTTON.draw(surface)
            
            SETTINGS_BUTTON = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 125, SETTINGS_IMG, 0.8)
            SETTINGS_BUTTON.draw(surface)

            EXIT_BUTTON = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 250, EXIT_IMG, 0.8)  # create button instance
            EXIT_BUTTON.draw(surface)

            # OR TRY FOLLOWING INSTEAD:
            # for button in [self.start_button, self.exit_button, self.settings_button]:
            #     button.draw(surface)


            # INPUT HANDLING
            if self.menu_exit_action == True:
                self.running, running = False, False

            ## EVENTS ##
            for event in pygame.event.get():
                if event.type == pygame.QUIT:                                                                               # exit game function
                    self.exit_action = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if START_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.mixer.Sound.play(MENU_SOUND)
                        pygame.mixer.music.stop()
                        self.running, running = False, False                                                                # quit all menus and this specific menu loop
                    if SETTINGS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        running = False
                        self.settings_menu(surface)
                    if EXIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.exit_action = True

            if self.exit_action == True:
                return self.exit_action

            ## INPUT ##
            self.get_input()
            
            # DISPLAY UPDATE
            pygame.display.update()                                                                                         # update the screen

    def settings_menu(self, surface):
        running = True
        while running:
            # DEFINING CONSTANT VARIABLES
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            # SETTING TEXT FOR SETTINGS MENU
            heading_text = "Settings Menu"

            # DEFINING TEXT VARIABLES
            headingtext = HEADINGTEXT.render(heading_text, True, (0, 0, 0)).convert_alpha()  # render a Small Text
            headingtextrect = headingtext.get_rect()                                                              # get a Rectangle of the small Text ( needed, to be able to place the text precisely )
            headingtextrect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 250)                                     # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )

            # DRAWING ON THE SURFACE
            surface.blit(BACKGROUND_IMG)
            surface.blit(headingtext, headingtextrect)

            ## INITIALIZING BUTTONS AND DRAWING THEM ##
            SETTINGS_INPUT_BUTTON = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 125, SETTINGS_IMG, 0.8)
            SETTINGS_INPUT_BUTTON.draw(surface)

            RETURN_BUTTON = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 250, RETURN_IMG, 0.8)
            RETURN_BUTTON.draw(surface)


            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_action = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if SETTINGS_INPUT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.settings_input_menu(surface)
                        running = False
                    if RETURN_BUTTON.checkForInput(MENU_MOUSE_POS):
                        running = False
                        self.main_menu(surface)
            
            if self.exit_action == True:
                return self.exit_action


            # INPUT
            self.get_input()

            # DISPLAY UPDATE
            pygame.display.update()


    def settings_input_menu(self, surface):
        running = True
        action = None
        while running:
            # INITIALIZING CONSTANT VARIABLES
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            # SETTING TEXTS FOR THE MENU
            heading_text = "Settings - Input"
            menu_toggle_text = "Toggle Menu"
            move_up_text = "Move Up"
            move_down_text = "Move Down"
            move_right_text = "Move Right"
            move_left_text = "Move Left"
            attention_text = "Joystick Support for changing input isn't supported yet"

            # DEFINING TEXT VARIABLES
            headingtext = HEADINGTEXT.render(heading_text, True, (0, 0, 0)).convert_alpha()                             # render a Heading Text
            headingtextrect = headingtext.get_rect()                                                                    # get a Rectangle of the small Text ( needed, to be able to place the text precisely )
            headingtextrect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 250)                                      # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )

            menu_toggletext = SMALLTEXT.render(menu_toggle_text, True, (0, 0, 0)).convert_alpha()
            menu_toggletextrect = menu_toggletext.get_rect()
            menu_toggletextrect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 175)

            move_uptext = SMALLTEXT.render(move_up_text, True, (0, 0, 0)).convert_alpha()
            move_uptextrect = move_uptext.get_rect()
            move_uptextrect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 95)

            move_downtext = SMALLTEXT.render(move_down_text, True, (0, 0, 0)).convert_alpha()
            move_downtextrect = move_uptext.get_rect()
            move_downtextrect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 15)

            move_righttext = SMALLTEXT.render(move_right_text, True, (0, 0, 0)).convert_alpha()
            move_righttextrect = move_uptext.get_rect()
            move_righttextrect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - -55)

            move_lefttext = SMALLTEXT.render(move_left_text, True, (0, 0, 0)).convert_alpha()
            move_lefttextrect = move_uptext.get_rect()
            move_lefttextrect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - -135)

            attentiontext = SMALLTEXT.render(attention_text, True, (0, 0, 0)).convert_alpha()
            attentiontextrect = attentiontext.get_rect()
            attentiontextrect.center = (WINDOW_WIDTH // 2 + 400, WINDOW_HEIGHT - -225)


            # DRAWING TO THE SURFACE
            surface.blit(BACKGROUND_IMG)
            surface.blit(headingtext, headingtextrect)
            surface.blit(menu_toggletext, menu_toggletextrect)
            surface.blit(move_uptext, move_uptextrect)
            surface.blit(move_downtext, move_downtextrect)
            surface.blit(move_righttext, move_righttextrect)
            surface.blit(move_lefttext, move_lefttextrect)
            surface.blit(attentiontext, attentiontextrect)

            ## DRAWING AND INITIALIZING BUTTONS ##
            RETURN_BUTTON = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 250, RETURN_IMG, 0.8)
            RETURN_BUTTON.draw(surface)

            MENU_TOGGLE_BUTTON = Button(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 180, TEST_IMG, 0.5)
            MENU_TOGGLE_BUTTON.draw(surface)

            MOVE_UP_BUTTON = Button(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 100, TEST_IMG, 0.5)
            MOVE_UP_BUTTON.draw(surface)

            MOVE_DOWN_BUTTON = Button(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 20, TEST_IMG, 0.5)
            MOVE_DOWN_BUTTON.draw(surface)

            MOVE_RIGHT_BUTTON = Button(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - -60, TEST_IMG, 0.5)
            MOVE_RIGHT_BUTTON.draw(surface)

            MOVE_LEFT_BUTTON = Button(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - -140, TEST_IMG, 0.5)
            MOVE_LEFT_BUTTON.draw(surface)


            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_action = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RETURN_BUTTON.checkForInput(MENU_MOUSE_POS):
                        running = False
                        self.settings_menu(surface)
                    if MENU_TOGGLE_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.get_pressed_keys_action = True
                        action = "menu_toggle"                      
                    if MOVE_UP_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.get_pressed_keys_action = True
                        action = "move_up"
                    if MOVE_DOWN_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.get_pressed_keys_action = True
                        action = "move_down"
                    if MOVE_RIGHT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.get_pressed_keys_action = True
                        action = "move_right"
                    if MOVE_LEFT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.get_pressed_keys_action = True
                        action = "move_left"

            if self.exit_action == True:
                return self.exit_action


            # INPUT
            self.get_input()                                                                                                                                    # input handling function for menu (joystick + keyboard support)                                                                                                          
            if action != None:                                                                                                                                  # if any of the button was pressed, do following:
                self.get_pressed_keys(action)                                                                                                                   # get user input and bound new key to an action

            # DISPLAY UPDATE
            pygame.display.update()  # update the screen
