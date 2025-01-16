######### IMPORT ##############

import pygame

from settings import *
from dialog import *

######### SPRITEs #############

# LISTS FOR LOADING SPRITES (ANIMATION)
## PLAYER'S SPRITES
PLAYER_R = [
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_right_still.png')),
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_right_walk_1.png')),
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_right_walk_2.png'))]

PLAYER_L = [
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_left_still.png')),
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_left_walk_1.png')),
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_left_walk_2.png'))]

PLAYER_B = [
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_back_still.png')),
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_back_walk_1.png')),
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_back_walk_2.png'))]

PLAYER_F = [
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_front_still.png')),
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_front_walk_1.png')),
    pygame.image.load(os.path.join('..', 'graphics', 'player', 'walk_animation', 'player_front_walk_2.png'))]

## NPC'S SPRITE/S
NPC_IDLE = pygame.image.load(os.path.join('..', 'graphics', 'player', 'idle', 'player_idle.png'))                                         # load sprite of the NPC (in action: idle) # for now it's the same image, but in the future there will be a separate one.


######### CLASSes ############

class Player(pygame.sprite.Sprite):
    def __init__(self, input, pos, groups, health=100):
        # ATTRIBUTES
        self.health = health                                                                                            # initialize new variable/attribute for the player (health)

        super().__init__(groups)                                                                                        # this subclass sets up the basic properties and methods that it inherits from its parent class (group)
        self.image = PLAYER_R[0].convert_alpha()                                                                        # assign image to the player # convert_alpha() function used to specify that the image should be rendered with alpha colors (for .png format)
        self.new_size_image = (self.image.get_width() * 4, self.image.get_height() * 4)                                 # declare new variable that has 4 times bigger scale than the player's image
        self.image = pygame.transform.scale(self.image, self.new_size_image)                                            # scale the image by 4 times
        self.rect = self.image.get_frect(center=pos)                                                                    # convert image to rectangle (needed for collision in the future), center is position that was provided during construction (__init__())
        self.input = input

        self.direction = vector()                                                                                       # create a table(vector2d) which has direction input for x and y coordinates. Example: (x, y). It looks similar to the tuple, but it is not immutable and the values in it can be changed
        self.current_direction = 'down'                                                                                 # initialize new variable that holds information of current direction that player is facing towards
        self.joystick_input_vector = None                                                                               # initializing joystick input vector variable and giving it a default value
        self.index = 0
        self.animation_speed = 5


    # INPUT FOR JOYSTICK LOGIC
    def input_joystick(self, axes_value=pygame.Vector2(0, 0), button_value=0):
        self.joystick_input_vector = pygame.Vector2(axes_value)                                                         # initialize joystick input vector variable which stores x and y axes/coordinates from sticks on the joystick
        self.direction = self.joystick_input_vector                                                                     # initialize direction variable, which includes x and y coordinates as a vector, which indicates the position, that player should be heading towards

    # MAIN INPUT LOGIC
    def input_logic(self):
        keys = pygame.key.get_pressed()                                                                                 # get user's input of just pressed keys
        keys_input_vector = vector()                                                                                    # create input vector for movement logic (by default, the value is (0,0), which responds to x and y coordinates)
        num_joysticks = pygame.joystick.get_count()

        # MOVEMENT
        if keys[self.input.key_bindings["move_up"]] or num_joysticks > 0 and (self.direction.y < 0 and (self.direction.y - self.direction.x) <= 0):
            keys_input_vector.y -= 1
            self.current_direction = 'up'
        if keys[self.input.key_bindings["move_down"]] or num_joysticks > 0 and (self.direction.y > 0 and (self.direction.y - self.direction.x) >= 0):
            keys_input_vector.y += 1
            self.current_direction = 'down'
        if keys[self.input.key_bindings["move_left"]] or num_joysticks > 0 and (self.direction.x < 0 and (self.direction.x - self.direction.y) <= 0):
            keys_input_vector.x -= 1
            self.current_direction = 'left'
        if keys[self.input.key_bindings["move_right"]] or num_joysticks > 0 and (self.direction.x > 0 and (self.direction.x - self.direction.y) >= 0):
            keys_input_vector.x += 1
            self.current_direction = 'right'

        # INPUT HANDLING / CHECKING IF THE KEYBOARD OR JOYSTICK SHOULD BE USED
        if self.joystick_input_vector == pygame.Vector2(0.0, 0.0) or self.joystick_input_vector == None or num_joysticks == 0:  # if connected joystick has no input, or no joysticks have been connected run following:
            if keys_input_vector != vector(0, 0) or keys_input_vector == vector(0, 0) and self.direction != vector(0, 0):  # if keyboard's key has been clicked and stores movement/position value, or if the key stores no movement position (0, 0), but the direction is still containing value inside, which means that the player is still moving, even though the key has been released, do following
                self.direction = keys_input_vector                                                                      # use keyboard's input for movement   # the upper if statement is needed, so that the player wouldn't continue running, even when the button/key has been long since released on the keyboard
        else:                                                                                                           # else do nothing
            pass                                                                                                        # do nothing

    def animation(self, dt):
        if self.current_direction == 'up':
            animation_frames = PLAYER_B
        elif self.current_direction == 'down':
            animation_frames = PLAYER_F
        elif self.current_direction == 'left':
            animation_frames = PLAYER_L
        elif self.current_direction == 'right':
            animation_frames = PLAYER_R
        else:
            animation_frames = PLAYER_F

        if self.direction.magnitude() != 0:                                                                             # run animation when the player moves (when vector isn't (0, 0))
            self.index += self.animation_speed * dt                                                                          # increment Frame-Index
            if self.index >= len(animation_frames):                                                                     # reset if the list ends
                self.index = 0
        else:
            self.index = 0                                                                                              # if the player stops, Frame-Index goes back to default value (0)

        self.image = pygame.transform.scale(animation_frames[int(self.index)].convert_alpha(), self.new_size_image)

    def move(self, dt):
        self.rect.center += self.direction * 250 * dt                                                                   # multiplying by dt = delta time (difference from last and next frame), so that our movement will be frame speed independent. It means it will not get faster or slower if fps changes.

    def update(self, dt):
        self.input_logic()
        self.animation(dt)
        self.move(dt)
        #print(self.input.key_bindings)


class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = NPC_IDLE.convert_alpha()
        self.new_size_image = (self.image.get_width() * 4, self.image.get_height() * 4)                                 # declare new variable that has 4 times bigger scale than the player's image
        self.image = (pygame.transform.scale(self.image, self.new_size_image))
        self.rect = self.image.get_frect(center=pos)                                                                    # convert image to rectangle (needed for collision in the future), center is position that was provided during construction (__init__())
        self.pos = pos

    def interact(self, text, player_center):
        self.player_center = player_center
        dialog = Dialog(self.pos)                                                                                       # initializing dialog class
        dialog.interact(text, self.player_center)                                                                       # run dialogs' interact function, to show some tex