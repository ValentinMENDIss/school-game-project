######### IMPORT ##############

import pygame

from settings import *
from dialog import *
from battle import Battle_Menu
from timer import Timer
from gamedata import NPC_ENEMY_DEFEATED_INTERACT_DATA

######### CLASSes ############

class Player(pygame.sprite.Sprite):
    def __init__(self, input, pos, groups, collision_sprites, health=100,stamina=100,defence=100,attack=100):
        # ATTRIBUTES
        self.health = health                                                                                            # initialize new variable/attribute for the player (health)
        self.stamina = stamina
        self.attack = attack
        self.defence = defence
        self.z = WORLD_LAYERS['main']
        self.collision_rects = [sprite.rect for sprite in collision_sprites if sprite is not self]
        self.collision_sprites = collision_sprites
        self.speed = 250                                                                                                # in-game attribute for speed

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
        self.y_sort = self.rect.centery
        self.hitbox = self.rect.inflate(-self.rect.width / 2, -60)                                                      # .inflate() : method that allows to change the size of a rectangle (hitbox is slightly smaller than whole image.rect)

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
        self.rect.centerx += self.direction.x * self.speed * dt                                                                   # multiplying by dt = delta time (difference from last and next frame), so that our movement will be frame speed independent. It means it will not get faster or slower if fps changes.
        self.hitbox.centerx = self.rect.centerx
        self.collisions('horizontal')

        self.rect.centery += self.direction.y * self.speed * dt
        self.hitbox.centery = self.rect.centery
        self.collisions('vertical')

    def collisions(self, axis):
        for sprite in self.collision_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if axis == 'horizontal':
                    if self.direction.x > 0: 
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                else:
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery

    def update(self, dt):
        self.y_sort = self.rect.centery
        self.input_logic()
        self.animation(dt)
        self.move(dt)


class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = NPC_IDLE.convert_alpha()
        self.new_size_image = (self.image.get_width() * 4, self.image.get_height() * 4)                                 # declare new variable that has 4 times bigger scale than the player's image
        self.image = (pygame.transform.scale(self.image, self.new_size_image))
        self.rect = self.image.get_frect(center=pos)                                                                    # convert image to rectangle (needed for collision in the future), center is position that was provided during construction (__init__())
        self.pos = pos
        self.z = WORLD_LAYERS['main']
        self.y_sort = self.rect.centery

    def interact(self, text, player_center):
        self.player_center = player_center
        dialog = Dialog(self.pos)                                                                                       # initializing dialog class
        dialog.interact(text, self.player_center)                                                                       # run dialogs' interact function, to show some tex

class NPC_Enemy(NPC):
    def __init__(self, pos, groups, health=100):
        super().__init__(pos, groups)
        self.image = NPC_IDLE.convert_alpha()
        self.new_size_image = (self.image.get_width() * 4, self.image.get_height() * 4)                                 # declare new variable that has 4 times bigger scale than the player's image
        self.image = (pygame.transform.scale(self.image, self.new_size_image))
        self.rect = self.image.get_frect(center=pos)                                                                    # convert image to rectangle (needed for collision in the future), center is position that was provided during construction (__init__())
        self.pos = pos
        self.z = WORLD_LAYERS['main']
        self.y_sort = self.rect.centery
        self.battle_menu = Battle_Menu()
        # ATTRIBUTES
        self.health = 100
        self.text = ""
        self.battle_menu = Battle_Menu(enemy_health=self.health, game=self.game)
        self.timer = Timer()



    def interact(self, surface, player_center):
        if self.health > 0:
            self.battle_menu.draw(surface)
            if self.battle_menu.enemy_health <= 0:
                self.health = 0
                self.game.action = None
        else:
            if self.timer.active == False and not self.timer.is_finished:
                self.timer.start(self.game.action_duration)
                self.text = self.game.get_random_interact_text(NPC_ENEMY_DEFEATED_INTERACT_DATA)
            if self.timer.is_finished:
                self.game.action = None
                self.timer.is_finished = False

            self.timer.update()
            self.player_center = player_center
            dialog = Dialog(self.pos)                                                                                       # initializing dialog class
            dialog.interact(self.text, self.player_center, screen=self.game.SCREEN)                                                                       # run dialogs' interact function, to show some tex