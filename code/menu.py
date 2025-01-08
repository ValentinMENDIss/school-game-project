######### IMPORT ##############
from settings import *
from button import *
from input import *

# LOADING IMAGES
BACKGROUND_IMG = pygame.image.load(os.path.join('..', 'graphics', 'background.png'))		                                # load image and use it as a menu background

######### CLASSES #############
class Menu:
    def __init__(self, game):
        self.game = game
        self.text = ""
        self.start_button = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, START_IMG, 0.8)  # create button instance
        self.exit_button = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 125, EXIT_IMG, 0.8)  # create button instance
        self.settings_input_button = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 250, SETTINGS_IMG, 0.8)
        self.return_button = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 250, RETURN_IMG, 0.8)
        self.running = True

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
        while running:
            # SETTING TEXT FOR MENU
            heading_text = "Settings - Input"

            # DEFINING TEXT VARIABLES
            headingtext = HEADINGTEXT.render(heading_text, True, (0, 0, 0)).convert_alpha()  # render a Small Text
            headingtextrect = headingtext.get_rect()  # get a Rectangle of the small Text ( needed, to be able to place the text precisely )
            headingtextrect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 250)  # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )

            # DRAWING TO SURFACE
            surface.blit(BACKGROUND_IMG)
            surface.blit(headingtext, headingtextrect)

            self.return_button.draw(surface)

            if self.return_button.action:
                self.main_menu(surface)
                running = False

            self.events()
            self.get_input()

            pygame.display.update()  # update the screen