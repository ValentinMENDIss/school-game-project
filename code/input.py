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
import pygame.event

from settings import *

######### CLASSes ############
class UserInput:
    def __init__(self, game):
        # VARIABLES
        self.joystick_button_pressed = False                                                                            # initialize variable that stores information of, if the joystick button has been already pressed and so counts to being hold
        self.game = game                                                                                                # import main game's logic variables and functions, so that they could be runned here
        self.key_bindings = {
            "move_left": pygame.K_LEFT,
            "move_right": pygame.K_RIGHT,
            "move_up": pygame.K_UP,
            "move_down": pygame.K_DOWN,
            "menu_toggle": pygame.K_ESCAPE,
            "shop_toggle": pygame.K_TAB
        }

    # GET USER INPUT
    def update(self):
        # GET USER'S INPUT
        self.get_input()

        # INPUT HANDLING/CHECKING
        if self.keys[pygame.K_e] or (self.num_joysticks > 0 and self.button_states[0] == 1 and self.joystick_button_pressed == False):   # if the key that was just pressed on the keyboard is 'E' or an 'A' Button on the joystick, do following:
            self.game.action = "item_pickup"
            # DIALOG SYSTEM

            for npc in self.game.npcs_on_current_screen:
                if abs(npc.rect[0] - self.game.player.rect[0]) <= 200 and abs(npc.rect[1] - self.game.player.rect[1]) <= 200:   # check NPC's and player's position. If the differences between each x and y value/coordinates is smaller in value then 200, do following:
                    pygame.mixer.Sound.play(YIPPEE_SOUND)                                                                   # play sound
                    self.game.npc_interact = npc 
                    self.game.action = "npc"

        if self.keys[self.key_bindings["menu_toggle"]] or (self.num_joysticks > 0 and self.button_states[7] == 1 and self.joystick_button_pressed == False):  # if the key that was just pressed on the keyboard is 'ESCAPE', do following:
            if self.game.menu_startup == False:
                self.button_state()
                self.game.current_screen = "menu"                                                                       # run menu logic

        self.button_state()

    # BUTTON STATE/PRESSED CHECKING                                                                                     # checking if the button is still pressed(hold) or not
    def button_state(self):
        if self.num_joysticks > 0:
            if any(self.button_states) and not self.joystick_button_pressed:                                            # if any button was just pressed, do following
                self.joystick_button_pressed = True                                                                     # set joystick_button_pressed variable to true, as the button has been pressed, and now if it continues to be pressed, it is being hold
            elif not any(self.button_states):                                                                           # else if no button was pressed, do following:
                self.joystick_button_pressed = False                                                                    # reset joystick_button_pressed variable to default value: False

    def get_input(self):
        # KEYBOARD INPUT
        self.keys = pygame.key.get_just_pressed()                                                                       # initialize new variable(keys) that will get user's input, but the buttons can be detected as pressed and not as hold too.

        # JOYSTICK INPUT
        pygame.joystick.init()                                                                                          # initialize pygame.joystick module

        # GET CONNECTED JOYSTICKS
        self.num_joysticks = pygame.joystick.get_count()                                                                # get number of currently connected joysticks to the computer
        if self.num_joysticks > 0:                                                                                      # if at least one gamepad/joystick has been connected to the pc, do following:
            self.my_joystick = pygame.joystick.Joystick(0)                                                              # select first connected joystick for input handling
            self.joystick_x_axis = self.my_joystick.get_axis(0)                                                         # get joystick's x-axis
            self.joystick_y_axis = self.my_joystick.get_axis(1)                                                         # get joystick's y-axis
            self.joystick_input_vector = (self.joystick_x_axis, self.joystick_y_axis)                                   # create input vector, that stores x and y-axis values in it
            self.button_states = [self.my_joystick.get_button(i) for i in range(self.my_joystick.get_numbuttons())]     # get the button states
            if abs(self.joystick_x_axis) < 0.1 and abs(self.joystick_y_axis) < 0.1:                                     # reset the joystick's input vector if the joystick isn't being moved anymore
                self.joystick_input_vector = pygame.Vector2(0, 0)                                                       # reset joystick's input vector to default. AKA (0, 0)
            try:
                self.game.player.input_joystick(axes_value=(self.joystick_input_vector), button_value=self.button_states)   # parse joystick's states to the input handling
            except AttributeError:
                print("No player Attribute")

    def menu(self):
        pygame.time.delay(10)                                                                                           # wait 10ms(milliseconds), for optimization purposes, so that it would not check the input every single it can render a frame

        self.menu_running = True                                                                                        # initialize variable that stores bool value and is needed to say if the menu should be running or not (needed for loop inside Menu() class)
        self.get_input()                                                                                                # get user's input

        if self.keys[self.key_bindings["menu_toggle"]] or (self.num_joysticks > 0 and self.button_states[7] == 1 and self.joystick_button_pressed == False):  # if the key that was just pressed on the keyboard is 'ESCAPE', or "A" button on the joystick do following:
            pygame.mixer.Sound.play(MENU_SOUND)
            self.menu_running = False                                                                                   # set value: False(bool) to the menu_running variable. The menu should be quited
        self.button_state()

    def menu_input(self, action):
        # GET USER'S INPUT AND USE IT FOR THE ACTION
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                new_key = event.key
                self.key_bindings[action] = new_key
                print(f"'{action}' is now bound to {pygame.key.name(new_key)}")
                return False
