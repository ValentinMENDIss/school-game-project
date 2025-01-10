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
        self.start_button = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, START_IMG, 0.8)  # create button instance
        self.exit_button = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 125, EXIT_IMG, 0.8)  # create button instance
        self.settings_input_button = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 250, SETTINGS_IMG, 0.8)
        self.return_button = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 250, RETURN_IMG, 0.8)
        self.running = True
        self.get_pressed_keys_action = False

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
            self.running = False

    def events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                #if event.type == pygame.KEYDOWN:
                    #print(event.key)
    # GET PRESSED KEYS
    def get_pressed_keys(self, action):
        if self.get_pressed_keys_action:
            self.game.menu_get_pressed_keys(action)

            if self.game.menu_get_pressed_keys(action) == False:
                self.get_pressed_keys_action = False


    def main_menu(self, surface):
        running = True
        while running:
            # SETTING TEXT FOR MENU
            heading_text = "Menu"

            # DEFINING TEXT VARIABLES
            headingtext = HEADINGTEXT.render(heading_text, True, (0, 0, 0)).convert_alpha()  # render a Small Text
            headingtextrect = headingtext.get_rect()                                                              # get a Rectangle of the small Text ( needed, to be able to place the text precisely )
            headingtextrect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 250)                                     # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )


            # DRAWING TO SURFACE
            surface.blit(BACKGROUND_IMG)
            surface.blit(headingtext, headingtextrect)

            self.start_button.draw(surface)

            self.exit_button.draw(surface)

            self.settings_input_button.draw(surface)

            if self.start_button.action:
                pygame.mixer.Sound.play(MENU_SOUND)
                pygame.mixer.music.stop()
                self.running, running = False, False
            if self.exit_button.action:
                self.exit_action = True
                return self.exit_action
            if self.settings_input_button.action:
                self.settings_input(surface)
                running = False

            if self.running == False:
                return self.running
                
            self.events()
            self.get_input()

            pygame.display.update()                                                                                         # update the screen



    def settings_input(self, surface):
        running = True
        action = None
        while running:
            # SETTING TEXT FOR MENU
            heading_text = "Settings - Input"
            menu_toggle_text = "Toggle Menu"
            attention_text = "Joystick Support for changing input isn't supported yet"

            # DEFINING TEXT VARIABLES
            headingtext = HEADINGTEXT.render(heading_text, True, (0, 0, 0)).convert_alpha()                             # render a Heading Text
            headingtextrect = headingtext.get_rect()                                                                    # get a Rectangle of the small Text ( needed, to be able to place the text precisely )
            headingtextrect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 250)                                      # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )

            menu_toggletext = SMALLTEXT.render(menu_toggle_text, True, (0, 0, 0)).convert_alpha()
            menu_toggletextrect = menu_toggletext.get_rect()
            menu_toggletextrect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 175)

            attentiontext = SMALLTEXT.render(attention_text, True, (0, 0, 0)).convert_alpha()
            attentiontextrect = attentiontext.get_rect()
            attentiontextrect.center = (WINDOW_WIDTH // 2 + 400, WINDOW_HEIGHT - 25)

            # DRAWING TO SURFACE
            surface.blit(BACKGROUND_IMG)
            surface.blit(headingtext, headingtextrect)
            surface.blit(menu_toggletext, menu_toggletextrect)
            surface.blit(attentiontext, attentiontextrect)

            ## DRAWING BUTTONS ##
            self.return_button.draw(surface)
            self.menu_toggle_button = Button(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 180, TEST_IMG, 0.5)
            self.menu_toggle_button.draw(surface)

            # CHECK CONDITIONS
            if self.return_button.action:
                self.main_menu(surface)
                running = False

            if self.menu_toggle_button.action:
                self.get_pressed_keys_action = True
                action = "menu_toggle"


            self.events()
            self.get_input()
            if action != None:
                self.get_pressed_keys(action)

            #menu_toggle_key = self.input.key_bindings["menu_toggle"]
            #print(pygame.key.name(menu_toggle_key))

            pygame.display.update()  # update the screen
