######### IMPORT ##############
from settings import *
from button import *

######### CLASSES #############
class Menu:
    def __init__(self):
        self.text = ""


    def draw(self, surface):
        # SETTING TEXT FOR MENU
        self.heading_text = "Menu"

        # DEFINING TEXT VARIABLES

        self.headingtext = HEADINGTEXT.render(self.heading_text, True, (0, 0, 0)).convert_alpha()  # render a Small Text
        self.headingtextrect = self.headingtext.get_rect()                                                              # get a Rectangle of the small Text ( needed, to be able to place the text precisely )
        self.headingtextrect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 250)                                     # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )


        # DRAWING TO SURFACE
        surface.fill((187, 180, 207))                                                                                   # Draw a white coloured Screen
        surface.blit(self.headingtext, self.headingtextrect)

        self.start_button = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, START_IMG, 0.8)                         # create button instance
        self.start_button.draw(surface)
        self.exit_button = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 125, EXIT_IMG, 0.8)                     # create button instance
        self.exit_button.draw(surface)

        pygame.display.update()                                                                                         # update the screen

    def show(self, surface):
        self.running = True
        self.exit_action = False

        while self.running:
            self.draw(surface)
            if self.start_button.action:
                pygame.mixer.Sound.play(MENU_SOUND)
                pygame.mixer.music.stop()                  
                self.running = False
            if self.exit_button.action:
                self.exit_action = True
                return self.exit_action
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:                       
                        self.running = False