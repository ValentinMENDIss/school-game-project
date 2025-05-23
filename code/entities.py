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

import pygame

from settings import *
from dialog import Dialog
from battle import Battle_Menu
from timer import Timer
from gamedata import NPC_ENEMY_DEFEATED_INTERACT_DATA, NPC_ENEMY_WON_INTERACT_DATA, NPC_DIALOG_1, SIDE_QUESTS
from savedata import load_saved_data, change_attribute
from gamedata import NPC_INTERACT_DATA

######### CLASSes ############

class Player(pygame.sprite.Sprite):
    initiated = False
    def __init__(self, input, pos, groups, collision_sprites, level=0, money=5):
        global initiated
        Player.initiated = True
        # ATTRIBUTES
        self.player_data = load_saved_data()
        self.health = self.player_data['health']                                                                                            # initialize new variable/attribute for the player (health)
        self.stamina = self.player_data['stamina']
        self.defence = self.player_data['defence']
        self.damage = self.player_data['damage']
        self.level = level
        self.money = money
        self.z = WORLD_LAYERS['main']
        self.collision_rects = [sprite.rect for sprite in collision_sprites if sprite is not self]
        self.collision_sprites = collision_sprites
        self.speed = 250                                                                                                # in-game attribute for speed
        self.active_quests = {}

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

    def teleport(self, pos):
        self.rect.centerx = pos[0]                                                                                               # change player's x coordinates
        self.hitbox.centerx = self.rect.centerx
        self.collisions('horizontal')

        self.rect.centery = pos[1]                                                                                               # change player's y coordinates
        self.hitbox.centery = self.rect.centery
        self.collisions('vertical')
        
        #if self.game.debug:
        #print("$##############")
        #print(pos[0], pos[1])
        #print(self.rect.centerx, self.rect.centery)
        #print("#############$")
        #self.rect = self.image.get_frect(center=pos)

    def update(self, dt):
        self.y_sort = self.rect.centery                                                                                         # variable that stores value for y_sort(position on y-axis)
        self.input_logic()                                                                                                      # run main input logic for player
        self.animation(dt)                                                                                                      # run animation method
        self.move(dt)                                                                                                           # move player to his new position

    def change_health(self, multiplier):
        new_health = self.health * multiplier
        self.health = new_health
        self.player_data['health'] = self.health                                                                        # Save the new value to savedata
        change_attribute('health', new_health, self.player_data)  # Persist the change

    def change_stamina(self, multiplier):
        new_stamina = self.stamina * multiplier
        self.stamina = new_stamina
        self.player_data['stamina'] = self.stamina
        change_attribute('stamina', new_stamina, self.player_data)

    def change_damage(self, multiplier):
        new_damage = self.damage * multiplier
        self.damage = new_damage
        self.player_data['damage'] = self.damage
        change_attribute('damage', new_damage, self.player_data)

    def change_defence(self, multiplier):
        new_defence = self.defence * multiplier
        self.defence = new_defence
        self.player_data['defence'] = self.defence
        change_attribute('defence', new_defence, self.player_data)

    def get_status(self):
        return {
            'health': self.health,
            'stamina': self.stamina,
            'damage': self.damage,
            'defence': self.defence
        }


class NPC(pygame.sprite.Sprite):
    def __init__(self, name, pos, groups, game, dialog_bool):
        super().__init__(groups)
        self.game = game
        self.image = NPC_IDLE.convert_alpha()
        self.new_size_image = (self.image.get_width() * 4, self.image.get_height() * 4)                                 # declare new variable that has 4 times bigger scale than the player's image
        self.image = (pygame.transform.scale(self.image, self.new_size_image))
        self.name = name
        self.rect = self.image.get_frect(center=pos)                                                                    # convert image to rectangle (needed for collision in the future), center is position that was provided during construction (__init__())
        self.pos = pos
        self.side_quests = self.get_side_quests()
        self.z = WORLD_LAYERS['main']
        self.y_sort = self.rect.centery
        self.show_interact_text = False
        self.dialog_bool = dialog_bool                                                                                  # dialog_bool is a 'flag', variable that stores value in form of boolean and says whether dialog should be used or plain text rendering when interacted with NPC
        self.timer = Timer()
        self.dialog = Dialog(self.pos, self.game)
        self.text = None
        self.quest_assignable = False                                                                                   # flag/variable that stores bool type value, and determines whether entity can give quest to the player
        self.speed = 250

    def move(self, dt, direction_x=0, direction_y=0):
        self.rect.centerx += direction_x * self.speed * dt                                                                   # multiplying by dt = delta time (difference from last and next frame), so that our movement will be frame speed independent. It means it will not get faster or slower if fps changes.
        self.rect.centery += direction_y * self.speed * dt
        self.pos = (self.rect.centerx, self.rect.centery)

    def get_side_quests(self):
        return SIDE_QUESTS.get(self.name, {})                                                                           # Retrieve the side quests from the SIDE_QUESTS dictionary located in gamedata.py based on the NPC's name
 
    def interactInRange(self, player_center, screen):
        player_distance = pygame.Vector2(self.game.player.rect.center).distance_to(self.rect.center)
        if player_distance < 200:
            self.show_interact_text = True
        else:
            self.show_interact_text = False

        if self.show_interact_text:
            self.dialog = Dialog(self.pos, self.game)
            self.dialog.interactInRange("", player_center, screen=self.game.display_surface)

    def interact(self, player_center):
        if self.timer.active == False and not self.timer.is_finished:
            self.check_npc_can_assign_quest()
            self.timer.start(self.game.action_duration)
            self.dialog = Dialog(self.pos, self.game)
            self.text = self.game.get_random_interact_text(NPC_INTERACT_DATA)
        if self.timer.is_finished:
            self.timer.is_finished = False
            self.timer.active = False
            self.game.action = None
        self.timer.update()
        self.show_interact_text = False                                                                                             # stop showing interaction possibility, that is being shown when the user is in range of NPC's interaction  (because of overlapping issues)
        if self.dialog_bool:
            self.dialog.interactDialog(NPC_DIALOG_1, screen=self.game.display_surface)
            self.game.action = None
        else:
            self.dialog.interact(self.text, player_center, screen=self.game.display_surface)                                                                       # run dialogs' interact function, to show some text

    def check_npc_can_assign_quest(self):
        if self.game.game_time.game_time.hour >= 7:
            self.quest_assignable = True

        if self.quest_assignable:
            for quest in self.side_quests:
                quest_already_in_use = False
                if len(self.game.player.active_quests) >= 1:
                    for active_quest in self.game.player.active_quests[self.name]:
                        if quest != active_quest: 
                            pass
                        elif quest == active_quest:
                            quest_already_in_use = True
                            continue
                    if quest_already_in_use == False:
                        self.add_quest(self.name, quest)
                        return
                else:
                    self.add_quest(self.name, quest, empty_quests_log=True)
                    return

    def add_quest(self, npc_name, quest, empty_quests_log=False):
        initialized_new_quest_dict = False

        if empty_quests_log:
            self.game.player.active_quests[npc_name] = [quest]
            initialized_new_quest_dict = True
        else:
            for entity in self.game.player.active_quests:
                if entity != npc_name:
                    pass
                elif entity == npc_name:
                    continue
                self.game.player.active_quests[npc_name] = [quest]    
                initialized_new_quest_dict = True

        if initialized_new_quest_dict == False:
            self.game.player.active_quests[npc_name].append(quest)
        print(f"New Quest Appended: {self.game.player.active_quests}")


class NPC_Friendly(NPC):
    def __init__(self, name, pos, groups, game, dialog_bool):
        super().__init__(name, pos, groups, game, dialog_bool)


class NPC_Enemy(NPC):
    def __init__(self, name, pos, groups, game, health=100, dialog_bool=False):
        super().__init__(name, pos, groups, game, dialog_bool)
        # ATTRIBUTES
        self.health = 100
        self.text = ""
        self.action = None

        self.battle_menu = Battle_Menu(enemy_health=self.health, game=self.game)
        self.timer = Timer()

    def interact(self, surface, player_center):
        if self.action == None:
            self.battle_menu.draw(surface)
            if self.battle_menu.enemy_health <= 0:
                self.action = "Defeated"
            if self.battle_menu.player_health <= 0:
                self.action = "Won"
            self.health = self.battle_menu.enemy_health
            self.game.action = None
        else:
            if self.timer.active == False and not self.timer.is_finished:
                self.timer.start(self.game.action_duration)
                if self.action == "Defeated":
                    self.text = self.game.get_random_interact_text(NPC_ENEMY_DEFEATED_INTERACT_DATA)
                elif self.action == "Won":
                    self.text = self.game.get_random_interact_text(NPC_ENEMY_WON_INTERACT_DATA)
            if self.timer.is_finished:
                self.game.action = None
                self.timer.is_finished = False

            self.show_interact_text = False
            self.timer.update()
            dialog = Dialog(self.pos, self.game)                                                                                       # initializing dialog class
            dialog.interact(self.text, player_center, screen=self.game.display_surface)                                                                       # run dialogs' interact function, to show some tex


class NPC_Shop(NPC):
    def __init__(self, name, pos, groups, game, dialog_bool):
        super().__init__(name, pos, groups, game, dialog_bool)
        
    def interact(self):
        self.game.current_screen = "shop"
