#    School-Game-Project - Adventure style school game
#    Copyright (C) 2025 Valentin Virstiuc <valentin.vir@proton.me>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


######### IMPORT ##############
import settings
from ui import Button, Slider, InputBox
from input import *
from savedata import save_data, default_data, load_saved_data

# LOADING IMAGE            if hasattr(self.game.npc_enemy):S
BACKGROUND_IMG = pygame.image.load(os.path.join('..', 'graphics', 'background', 'background.png'))		                            # load image and use it as a menu background

######### CLASSES #############
class Menu:
    def __init__(self, game):
        pygame.init()                                                                                                   # initialize pygame framework
        self.game = game                                                                                                # declare variable that stores values from game() Class
        self.text = ""                                                                                                  # text variable
        self.running = True                                                                                             # loop value
        self.get_pressed_keys_action = False
        self.menu_exit_action = False
        self.current_screen = "main_menu"
        self.startup = None

    # DRAWING LOGIC
    def show(self, surface, startup=False):
        self.startup = startup
        self.running = True
        self.exit_action = False
        if self.current_screen == "main_menu":
            self.main_menu(surface)                                                                                     # draw main menu
        if self.exit_action:                                                                                        # if exit button is pressed, do following:
            self.game.current_screen = "game"

    # GET USER'S INPUT
    def get_input(self):
        self.input = self.game.input
        self.input.menu()                                                                                               # get input (function called from input class)
        if self.input.menu_running == False:                                                                            # if user is willing to exit menu, do following
            self.menu_exit_action = True                                                                                # exit (set menu_exit_action variable to True)
        else:                                                                                                           # else, do following:
            self.menu_exit_action = False                                                                               # set exit_action variable to default (False)

    # GET PRESSED KEYS
    def get_pressed_keys(self, action):
        if self.get_pressed_keys_action:                                                                                # if any key has been pressed, do following
            self.game.menu_get_pressed_keys(action)                                                                     # get pressed keys
            if self.game.menu_get_pressed_keys(action) == False:
                self.get_pressed_keys_action = False

    # MAIN MENU
    def main_menu(self, surface):
        ## INITIALIZING BUTTONS ##
        START_BUTTON = Button(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2, scale=0.8, image=START_IMG, hovered_image=START_IMG_PRESSED)  # create button instance
        SETTINGS_BUTTON = Button(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2 + 125, scale=0.8, image=SETTINGS_IMG, hovered_image=SETTINGS_IMG_PRESSED)
        EXIT_BUTTON = Button(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2 + 250, scale=0.8, image=EXIT_IMG, hovered_image=EXIT_IMG_PRESSED)  # create button instance
        self.game.music.pause()
        running = True
        while running:
            # DEFINING CONSTANT VARIABLES
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            # SETTING TEXT FOR MENU
            heading_text = "Menu"

            # DEFINING TEXT VARIABLES
            headingtext = HEADINGTEXT.render(heading_text, True, (0, 0, 0)).convert_alpha()  # render a Small Text
            headingtextrect = headingtext.get_rect()                                                              # get a Rectangle of the small Text ( needed, to be able to place the text precisely )
            headingtextrect.center = (settings.WINDOW_WIDTH // 2,settings.WINDOW_HEIGHT // 2 - 250)                                     # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )

            # DRAWING ON THE SURFACE
            surface.blit(BACKGROUND_IMG)
            surface.blit(headingtext, headingtextrect)

            ## DRAWING BUTTONS ##
            for button in [START_BUTTON, SETTINGS_BUTTON, EXIT_BUTTON]:
                button.draw(surface)

            # INPUT HANDLING
            if self.menu_exit_action == True:
                running = False
                self.game.current_screen = "game"

            ## EVENTS ##
            for event in pygame.event.get():
                if event.type == pygame.QUIT:                                                                               # exit game function
                    self.exit_action = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if START_BUTTON.checkForInput(MENU_MOUSE_POS):
                        if self.startup:
                            self.session_manager(surface)
                        pygame.mixer.Sound.play(MENU_SOUND)
                        running = False                                                                # quit all menus and this specific menu loop
                        self.game.current_screen = "game"
                    if SETTINGS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        running = False
                        self.settings(surface)
                    if EXIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.exit_action = True

            if self.exit_action == True:
                return self.exit_action

            # DISPLAY UPDATE
            pygame.display.update()                                                                                         # update the screen

    def session_manager(self, surface):
        NEW_SAVE_BUTTON = Button(settings.WINDOW_WIDTH // 2,settings.WINDOW_HEIGHT // 2, scale=0.8, image=INPUT_IMG, hovered_image=INPUT_IMG_PRESSED)
        LOAD_SAVE_BUTTON = Button(settings.WINDOW_WIDTH // 2,settings.WINDOW_HEIGHT // 2 + 125, scale=0.8, image=INPUT_IMG, hovered_image=INPUT_IMG_PRESSED)
        running = True
        while running:
            # DEFINING CONSTANT VARIABLES
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            # SETTING TEXT FOR SETTINGS MENU
            heading_text = "Session Manager"

            # DEFINING TEXT VARIABLES
            headingtext = HEADINGTEXT.render(heading_text, True, (0, 0, 0)).convert_alpha()  # render a Small Text
            headingtextrect = headingtext.get_rect()                                                              # get a Rectangle of the small Text ( needed, to be able to place the text precisely )
            headingtextrect.center = (settings.WINDOW_WIDTH // 2,settings.WINDOW_HEIGHT // 2 - 250)                                     # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )

            # DRAWING ON THE SURFACE
            surface.blit(BACKGROUND_IMG)
            surface.blit(headingtext, headingtextrect)

            ## DRAWING BUTTONS ##
            for button in [NEW_SAVE_BUTTON, LOAD_SAVE_BUTTON]:
                button.draw(surface)

            # INPUT HANDLING
            if self.menu_exit_action == True:
                self.running, running = False, False

            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_action = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if NEW_SAVE_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.new_save()
                        running = False
                        self.game.current_screen = "game"
                    if LOAD_SAVE_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.load_save()
                        running = False
                        self.game.current_screen = "game"

            if self.exit_action == True:
                return self.exit_action

            # INPUT
            self.get_input()

            # DISPLAY UPDATE
            pygame.display.update()


    def new_save(self):
        default_data()

    def load_save(self):
        load_saved_data()

    # SETTINGS MENU
    def settings(self, surface):
        ## INITIALIZING BUTTONS ##
        SETTINGS_VIDEO_BUTTON = Button(settings.WINDOW_WIDTH // 2,settings.WINDOW_HEIGHT // 2 - 125, scale=0.8, image=VIDEO_IMG, hovered_image=VIDEO_IMG_PRESSED)
        SETTINGS_INPUT_BUTTON = Button(settings.WINDOW_WIDTH // 2,settings.WINDOW_HEIGHT // 2, scale=0.8, image=INPUT_IMG, hovered_image=INPUT_IMG_PRESSED)
        SETTINGS_SOUND_BUTTON = Button(settings.WINDOW_WIDTH // 2,settings.WINDOW_HEIGHT // 2 + 125, scale=0.8, image=SOUNDS_IMG, hovered_image=SOUNDS_IMG_PRESSED)
        RETURN_BUTTON = Button(settings.WINDOW_WIDTH // 2,settings.WINDOW_HEIGHT // 2 + 250, scale=0.8,  image=RETURN_IMG, hovered_image=RETURN_IMG_PRESSED)
        running = True
        while running:
            # DEFINING CONSTANT VARIABLES
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            # SETTING TEXT FOR SETTINGS MENU
            heading_text = "Settings Menu"

            # DEFINING TEXT VARIABLES
            headingtext = HEADINGTEXT.render(heading_text, True, (0, 0, 0)).convert_alpha()  # render a Small Text
            headingtextrect = headingtext.get_rect()                                                              # get a Rectangle of the small Text ( needed, to be able to place the text precisely )
            headingtextrect.center = (settings.WINDOW_WIDTH // 2,settings.WINDOW_HEIGHT // 2 - 250)                                     # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )

            # DRAWING ON THE SURFACE
            surface.blit(BACKGROUND_IMG)
            surface.blit(headingtext, headingtextrect)

            ## DRAWING BUTTONS ##
            for button in [SETTINGS_VIDEO_BUTTON, SETTINGS_INPUT_BUTTON, SETTINGS_SOUND_BUTTON, RETURN_BUTTON]:
                button.draw(surface)

            # INPUT HANDLING
            if self.menu_exit_action == True:
                self.running, running = False, False

            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_action = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if SETTINGS_VIDEO_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.settings_video(surface)
                        running = False
                    if SETTINGS_INPUT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.settings_input(surface)
                        running = False
                    if SETTINGS_SOUND_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.settings_sound(surface)
                        running = False
                    if RETURN_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.main_menu(surface)
                        running = False

            if self.exit_action == True:
                return self.exit_action


            # INPUT
            self.get_input()

            # DISPLAY UPDATE
            pygame.display.update()


    def settings_video(self, surface):
        ## INITIALIZING BUTTONS ##
        HORIZONTAL_RESOLUTION_INPUT_BOX = InputBox(settings.WINDOW_WIDTH // 2 - 100,settings.WINDOW_HEIGHT // 2 - 100, width=100, height=50, initial_value=settings.WINDOW_WIDTH, centered=True)
        VERTICAL_RESOLUTION_INPUT_BOX = InputBox(settings.WINDOW_WIDTH // 2 + 210,settings.WINDOW_HEIGHT // 2 - 100, width=100, height=50, initial_value=settings.WINDOW_HEIGHT, centered=True)
        FPS_INPUT_BOX = InputBox(settings.WINDOW_WIDTH // 2 - 100,settings.WINDOW_HEIGHT // 2 - 20, width=100, height=50, initial_value=self.game.fps_lock, centered=True)
        RETURN_BUTTON = Button(settings.WINDOW_WIDTH // 2,settings.WINDOW_HEIGHT // 2 + 250, scale=0.5, image=RETURN_IMG, hovered_image=RETURN_IMG_PRESSED)
        # DEFINING VARIABLES
        running = True
        action = None
        while running:
            # INITIALIZING CONSTANT VARIABLES
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            # SETTING TEXT FOR SETTINGS MENU
            heading_text = "Settings - Video"
            horizontal_resolution_text = "Horizontal Resolution"
            vertical_resolution_text = "Vertical Resolution"
            fps_lock_text = "FPS Limit"

            # DEFINING TEXT VARIABLES
            headingtext = HEADINGTEXT.render(heading_text, True, (0, 0, 0)).convert_alpha()  # render a Small Text
            headingtextrect = headingtext.get_rect()                                                              # get a Rectangle of the small Text ( needed, to be able to place the text precisely )
            headingtextrect.center = (settings.WINDOW_WIDTH // 2,settings.WINDOW_HEIGHT // 2 - 250)                                     # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )
            
            horizontal_resolutiontext = SMALLTEXT.render(horizontal_resolution_text, True, (0, 0, 0)).convert_alpha()  # render a Small Text
            horizontal_resolutiontextrect = horizontal_resolutiontext.get_rect()                                                              # get a Rectangle of the small Text ( needed, to be able to place the text precisely )
            horizontal_resolutiontextrect.topleft = (settings.WINDOW_WIDTH // 2 - 35,settings.WINDOW_HEIGHT // 2 - 106)                                     # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )
            
            vertical_resolutiontext = SMALLTEXT.render(vertical_resolution_text, True, (0, 0, 0)).convert_alpha()  # render a Small Text
            vertical_resolutiontextrect = vertical_resolutiontext.get_rect()                                                              # get a Rectangle of the small Text ( needed, to be able to place the text precisely )
            vertical_resolutiontextrect.topleft = (settings.WINDOW_WIDTH // 2 + 275,settings.WINDOW_HEIGHT // 2 - 106)                                     # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )
 
            fps_locktext = SMALLTEXT.render(fps_lock_text, True, (0, 0, 0)).convert_alpha()
            fps_locktextrect = fps_locktext.get_rect()
            fps_locktextrect.topleft = (settings.WINDOW_WIDTH // 2 - 35,settings.WINDOW_HEIGHT // 2 - 25)


            # DRAWING ON THE SURFACE
            surface.blit(BACKGROUND_IMG)
            surface.blit(headingtext, headingtextrect)
            surface.blit(horizontal_resolutiontext, horizontal_resolutiontextrect)
            surface.blit(vertical_resolutiontext, vertical_resolutiontextrect)
            surface.blit(fps_locktext, fps_locktextrect)

            ## DRAWING BUTTONS ##
            for button in [RETURN_BUTTON]:
                button.draw(surface)
            for input_box in [HORIZONTAL_RESOLUTION_INPUT_BOX, VERTICAL_RESOLUTION_INPUT_BOX, FPS_INPUT_BOX]:
                input_box.draw(surface)

            # INPUT HANDLING
            if self.menu_exit_action == True:
                self.running, running = False, False

            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_action = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RETURN_BUTTON.checkForInput(MENU_MOUSE_POS):
                        running = False
                        self.settings(surface)
                    HORIZONTAL_RESOLUTION_INPUT_BOX.checkForInput(MENU_MOUSE_POS)
                    VERTICAL_RESOLUTION_INPUT_BOX.checkForInput(MENU_MOUSE_POS)
                    FPS_INPUT_BOX.checkForInput(MENU_MOUSE_POS)
                if event.type == pygame.KEYDOWN:
                    if HORIZONTAL_RESOLUTION_INPUT_BOX.pressed == True:
                        new_horizontal_resolution = HORIZONTAL_RESOLUTION_INPUT_BOX.update_value(event)
                        if new_horizontal_resolution == None:
                            new_horizontal_resolution == 1280
                        if new_horizontal_resolution:
                            self.game.change_resolution(new_horizontal_resolution, settings.WINDOW_HEIGHT)
                            HORIZONTAL_RESOLUTION_INPUT_BOX = InputBox(settings.WINDOW_WIDTH // 2 - 100,settings.WINDOW_HEIGHT // 2 - 100, width=100, height=50, initial_value=settings.WINDOW_WIDTH, centered=True)
                            VERTICAL_RESOLUTION_INPUT_BOX = InputBox(settings.WINDOW_WIDTH // 2 + 210,settings.WINDOW_HEIGHT // 2 - 100, width=100, height=50, initial_value=settings.WINDOW_HEIGHT, centered=True)
                            FPS_INPUT_BOX = InputBox(settings.WINDOW_WIDTH // 2 - 100,settings.WINDOW_HEIGHT // 2 - 20, width=100, height=50, initial_value=self.game.fps_lock, centered=True)
                            RETURN_BUTTON = Button(settings.WINDOW_WIDTH // 2,settings.WINDOW_HEIGHT // 2 + 250, scale=0.5, image=RETURN_IMG, hovered_image=RETURN_IMG_PRESSED)

                    if VERTICAL_RESOLUTION_INPUT_BOX.pressed == True:
                        new_vertical_resolution = VERTICAL_RESOLUTION_INPUT_BOX.update_value(event)
                        if new_vertical_resolution == None:
                            new_vertical_resolution == 720
                        if new_vertical_resolution:
                            self.game.change_resolution(settings.WINDOW_WIDTH, new_vertical_resolution)
                            HORIZONTAL_RESOLUTION_INPUT_BOX = InputBox(settings.WINDOW_WIDTH // 2 - 100,settings.WINDOW_HEIGHT // 2 - 100, width=100, height=50, initial_value=settings.WINDOW_WIDTH, centered=True)
                            VERTICAL_RESOLUTION_INPUT_BOX = InputBox(settings.WINDOW_WIDTH // 2 + 210,settings.WINDOW_HEIGHT // 2 - 100, width=100, height=50, initial_value=settings.WINDOW_HEIGHT, centered=True)
                            FPS_INPUT_BOX = InputBox(settings.WINDOW_WIDTH // 2 - 100,settings.WINDOW_HEIGHT // 2 - 20, width=100, height=50, initial_value=self.game.fps_lock, centered=True)
                            RETURN_BUTTON = Button(settings.WINDOW_WIDTH // 2,settings.WINDOW_HEIGHT // 2 + 250, scale=0.5, image=RETURN_IMG, hovered_image=RETURN_IMG_PRESSED)

                    if FPS_INPUT_BOX.pressed == True:
                        new_fps_lock = FPS_INPUT_BOX.update_value(event)
                        if new_fps_lock == None:
                            new_fps_lock = 60
                        self.game.fps_lock = new_fps_lock

            if self.exit_action == True:
                return self.exit_action

            # INPUT
            self.get_input()

            # DISPLAY UPDATE
            pygame.display.update()


    # INPUT SETTINGS MENU
    def settings_input(self, surface):
        ## INITIALIZING BUTTONS ##
        RETURN_BUTTON = Button(settings.WINDOW_WIDTH // 2,settings.WINDOW_HEIGHT // 2 + 250, scale=0.5, image=RETURN_IMG, hovered_image=RETURN_IMG_PRESSED)
        MENU_TOGGLE_BUTTON = Button(settings.WINDOW_WIDTH // 2 - 100,settings.WINDOW_HEIGHT // 2 - 180, scale=0.5, image=TEST_IMG, hovered_image=TEST_IMG_PRESSED)
        MOVE_UP_BUTTON = Button(settings.WINDOW_WIDTH // 2 - 100,settings.WINDOW_HEIGHT // 2 - 100, scale=0.5, image=TEST_IMG, hovered_image=TEST_IMG_PRESSED)
        MOVE_DOWN_BUTTON = Button(settings.WINDOW_WIDTH // 2 - 100,settings.WINDOW_HEIGHT // 2 - 20, scale=0.5, image=TEST_IMG, hovered_image=TEST_IMG_PRESSED)
        MOVE_RIGHT_BUTTON = Button(settings.WINDOW_WIDTH // 2 - 100,settings.WINDOW_HEIGHT // 2 - -60, scale=0.5, image=TEST_IMG, hovered_image=TEST_IMG_PRESSED)
        MOVE_LEFT_BUTTON = Button(settings.WINDOW_WIDTH // 2 - 100,settings.WINDOW_HEIGHT // 2 - -140, scale=0.5, image=TEST_IMG, hovered_image=TEST_IMG_PRESSED)
        # DEFINING VARIABLES
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
            headingtextrect.center = (settings.WINDOW_WIDTH // 2,settings.WINDOW_HEIGHT // 2 - 250)                                      # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )

            menu_toggletext = SMALLTEXT.render(menu_toggle_text, True, (0, 0, 0)).convert_alpha()
            menu_toggletextrect = menu_toggletext.get_rect()
            menu_toggletextrect.center = (settings.WINDOW_WIDTH // 2,settings.WINDOW_HEIGHT // 2 - 175)

            move_uptext = SMALLTEXT.render(move_up_text, True, (0, 0, 0)).convert_alpha()
            move_uptextrect = move_uptext.get_rect()
            move_uptextrect.center = (settings.WINDOW_WIDTH // 2,settings.WINDOW_HEIGHT // 2 - 95)

            move_downtext = SMALLTEXT.render(move_down_text, True, (0, 0, 0)).convert_alpha()
            move_downtextrect = move_uptext.get_rect()
            move_downtextrect.center = (settings.WINDOW_WIDTH // 2,settings.WINDOW_HEIGHT // 2 - 15)

            move_righttext = SMALLTEXT.render(move_right_text, True, (0, 0, 0)).convert_alpha()
            move_righttextrect = move_uptext.get_rect()
            move_righttextrect.center = (settings.WINDOW_WIDTH // 2,settings.WINDOW_HEIGHT // 2 - -55)

            move_lefttext = SMALLTEXT.render(move_left_text, True, (0, 0, 0)).convert_alpha()
            move_lefttextrect = move_uptext.get_rect()
            move_lefttextrect.center = (settings.WINDOW_WIDTH // 2,settings.WINDOW_HEIGHT // 2 - -135)

            attentiontext = SMALLTEXT.render(attention_text, True, (0, 0, 0)).convert_alpha()
            attentiontextrect = attentiontext.get_rect()
            attentiontextrect.center = (settings.WINDOW_WIDTH // 2 + 400,settings.WINDOW_HEIGHT - -225)


            # DRAWING TO THE SURFACE
            surface.blit(BACKGROUND_IMG)
            surface.blit(headingtext, headingtextrect)
            surface.blit(menu_toggletext, menu_toggletextrect)
            surface.blit(move_uptext, move_uptextrect)
            surface.blit(move_downtext, move_downtextrect)
            surface.blit(move_righttext, move_righttextrect)
            surface.blit(move_lefttext, move_lefttextrect)
            surface.blit(attentiontext, attentiontextrect)

            ## DRAWING BUTTONS ##
            for button in [RETURN_BUTTON, MENU_TOGGLE_BUTTON, MOVE_UP_BUTTON, MOVE_DOWN_BUTTON, MOVE_RIGHT_BUTTON, MOVE_LEFT_BUTTON]:
                button.draw(surface)

            # INPUT HANDLING
            if self.menu_exit_action == True:
                self.running, running = False, False

            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_action = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RETURN_BUTTON.checkForInput(MENU_MOUSE_POS):
                        running = False
                        self.settings(surface)
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


    def settings_sound(self, surface):
        ## INITIALIZING BUTTONS ##
        RETURN_BUTTON = Button(settings.WINDOW_WIDTH // 2,settings.WINDOW_HEIGHT // 2 + 250, scale=0.5, image=RETURN_IMG, hovered_image=RETURN_IMG_PRESSED)
        VOLUME_SLIDER = Slider(settings.WINDOW_WIDTH // 2,settings.WINDOW_HEIGHT // 2, width=500, height=25, min_value=0, max_value=1, initial_value=self.game.music.volume, centered=True)
        # DEFINING VARIABLES
        running = True
        while running:
            # DEFINING CONSTANT VARIABLES
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            # SETTING TEXT FOR SETTINGS MENU
            heading_text = "Settings - Sound"

            # DEFINING TEXT VARIABLES
            headingtext = HEADINGTEXT.render(heading_text, True, (0, 0, 0)).convert_alpha()  # render a Small Text
            headingtextrect = headingtext.get_rect()                                                              # get a Rectangle of the small Text ( needed, to be able to place the text precisely )
            headingtextrect.center = (settings.WINDOW_WIDTH // 2,settings.WINDOW_HEIGHT // 2 - 250)                                     # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )

            # DRAWING ON THE SURFACE
            surface.blit(BACKGROUND_IMG)
            surface.blit(headingtext, headingtextrect)

            for button in [RETURN_BUTTON]:
                button.draw(surface)
            for slider in [VOLUME_SLIDER]:
                slider.draw(surface)


            # INPUT HANDLING
            if self.menu_exit_action == True:
                self.running, running = False, False

            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_action = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RETURN_BUTTON.checkForInput(MENU_MOUSE_POS):
                        running = False
                    VOLUME_SLIDER.checkForInput(mouse_pos=MENU_MOUSE_POS, pressed_button=event.button)
                    self.game.music.set_volume(VOLUME_SLIDER.value)
                
            # INPUT
            self.get_input()                                                                                                                                    # input handling function for menu (joystick + keyboard support)

            if self.exit_action == True:
                return self.exit_action

            # DISPLAY UPDATE
            pygame.display.update()  # update the screen
