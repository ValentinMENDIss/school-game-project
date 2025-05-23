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
import random

import settings
import utils
from gamedata import NPC_ENEMY_INTERACT_DATA
from ui import Button
from timer import Timer
from savedata import change_player_data, load_saved_data

######### SPRITES ##############

BACKGROUND_IMG = pygame.image.load(settings.os.path.join('..', 'graphics', 'background', 'battle-menu-background.png'))

######### CLASSes ##############

class Battle_Menu:
    def __init__(self, enemy_health, game):
        self.game = game                                                                                                                    # declare new variable that stores main.py (Game()) loop's attributes and variables
        self.attack_type = ["attack", "emotional_attack"]                                                                                   # declare attack types
        self.items_dict = {}
        self.current_display = "battle_menu"
        self.items_menu_dict_update = False
        self.get_pressed_keys_action = False                                                                                                # variable that stores Bool value. Checks if action should be called
        self.exit_action = False                                                                                                            # variable that stores Bool value. Checks if action should be called
        self.show_player_damage_action = False                                                                                              # variable that stores Bool value. Checks if action should be called
        self.show_enemy_damage_action = False                                                                                               # variable that stores Bool value. Checks if action should be called
        self.enemy_health = enemy_health                                                                                                    # enemy's health
        self.player_data = game.saved_data
        self.player_health = self.player_data['health']                                                                                        # player's health
        self.player_stamina = self.player_data['stamina']
        self.player_damage = self.player_data['damage']
        self.player_defence = self.player_data['defence']
        
        self.damage = 0                                                                                                                     # variable that stores dealt damage in one round
        self.is_running = True
        self.FightButtonMenu = False
        # ACTION
        self.defence_action = False
        self.action = None
        self.action_start_time = 0
        self.action_duration = 2000
        # IMAGES
        self.enemy_image = settings.NPC_IDLE.convert_alpha()
        self.enemy_new_size_image = (self.enemy_image.get_width() * 4, self.enemy_image.get_height() * 4)                                 # declare new variable that has 4 times bigger scale than the player's image
        self.enemy_image = (pygame.transform.scale(self.enemy_image, self.enemy_new_size_image))
        # TEXTs
        self.enemytext = ""
        self.damagetext = ""
        # DEFINING CLASS VARIABLES
        self.timer = Timer()

    def random_text(self):
        if self.enemy_health <= 0:
            self.enemytext = "Congratulations, You've won me..."
        else:
            index = random.randint(0, len(NPC_ENEMY_INTERACT_DATA) - 1)
            self.enemytext = NPC_ENEMY_INTERACT_DATA[index]

    def attack_enemy(self, attack_type):
        if attack_type == "attack" and self.player_stamina >= 10:
            self.player_damage = random.randint(0, 25)
            self.enemy_health -= self.player_damage
            self.random_text()
            self.player_stamina -= 10
            self.player_defence -= 0.5
        elif attack_type == "emotional_attack" and self.player_stamina >= 5:
            self.player_damage = random.randint(0, 15)
            self.enemy_health -= self.player_damage
            self.random_text()
            self.player_stamina -= 5
            self.player_defence -= 0.25
        
        if self.player_stamina > 5:
            self.show_player_damage_action = True
            self.defence_action = False
            self.action = "Enemy_Fight"                                                                          # after player's fight, set action variable that corresponds to fight for NPC_ENEMY

    def defence(self):
        self.player_stamina += 10 
        self.defence_action = True
        if self.player_stamina > 100:
            self.player_stamina = 100
        if self.player_defence < 25:
            self.player_defence += 1
        self.action = "Enemy_Fight"                                                                          # after player's fight, set action variable that corresponds to fight for NPC_ENEMY

    # SHOW DEALT DAMAGE ON THE SCREEN
    def show_player_damage(self, surface):
        utils.render_text(surface, text=self.player_damage, pos_x=(settings.WINDOW_WIDTH//2+350), pos_y=220, color=(210,39,48), size=25)

    def show_enemy_damage(self, surface):
        utils.render_text(surface, self.enemy_damage, pos_x=340, pos_y=(settings.WINDOW_HEIGHT-250), color=(210,39,48), size=25)

    def attack_player(self):
        index = random.randint(0, len(self.attack_type) - 1)
        attack_type = self.attack_type[index]
        if attack_type == "attack":
            self.enemy_damage = random.randint(0, 25)
        if attack_type == "emotional_attack":
            self.enemy_damage = random.randint(0, 15)
        if self.defence_action:
            player_defence_chance = random.randint(0, 3)
            if player_defence_chance == 2:
                self.enemy_damage -= self.player_defence
                if self.enemy_damage < 0:
                    self.enemy_damage = 0
                print("Player's defence worked out!")
            else:
                print("Player's defence didn't worked out!")
        else:
            player_defence_chance = random.randint(0, 10)
            if player_defence_chance == 5:
                self.enemy_damage -= self.player_defence
                if self.enemy_damage < 0:
                    self.enemy_damage = 0
                print("Player's defence worked out!")
            else:
                print("Player's defence didn't worked out!")
               

        self.player_health -= self.enemy_damage
        self.show_enemy_damage_action = True

    def show_player_stamina(self, surface):
        utils.render_text(surface, text=self.player_stamina, pos_x=440, pos_y=(settings.WINDOW_HEIGHT-220), color=(255,215,0), size=35)

    def show_player_defence(self, surface):
        utils.render_text(surface, self.player_defence, pos_x=390, pos_y=(settings.WINDOW_HEIGHT-220), color=(0,181,226), size=35)

    def show_player_health(self, surface):
        utils.render_text(surface, self.player_health, pos_x=340, pos_y=(settings.WINDOW_HEIGHT-220), color=(4,106,56), size=35)


    # DRAWING LOGIC
    def draw(self, surface):
        self.is_running = True
        self.items_menu_dict_update = False
        self.game.music.pause()
        while self.is_running:
            if self.current_display == "battle_menu":
                self.battle_menu(surface)
                self.items_menu_dict_update = True
            elif self.current_display == "items_menu":
                self.items_menu(surface)
            else:
                self.items_menu_dict_update = False


    def battle_menu(self, surface):
        # INITIALIZING BUTTONS
        SURRENDER_BUTTON = Button(settings.WINDOW_WIDTH - 150, settings.WINDOW_HEIGHT - 100, scale=0.40, image=settings.SURRENDER_IMG, hovered_image=settings.SURRENDER_IMG_PRESSED)                             # create button instance
        FIGHT_BUTTON = Button(150, settings.WINDOW_HEIGHT - 100, scale=0.40, image=settings.START_IMG, hovered_image=settings.START_IMG_PRESSED)
        DEFENSE_BUTTON = Button(400, settings.WINDOW_HEIGHT - 100, scale=0.40, image=settings.START_IMG, hovered_image=settings.START_IMG_PRESSED)
        ITEMS_BUTTON = Button(650, settings.WINDOW_HEIGHT - 100, scale=0.40, image=settings.START_IMG, hovered_image=settings.START_IMG_PRESSED)
        SPELL_BUTTON = Button(900, settings.WINDOW_HEIGHT - 100, scale=0.40, image=settings.START_IMG, hovered_image=settings.START_IMG_PRESSED)
        EMOTIONAL_ATTACK_BUTTON = Button(150, settings.WINDOW_HEIGHT - 175, scale=0.40, image=settings.START_IMG, hovered_image=settings.START_IMG_PRESSED)
        ATTACK_BUTTON = Button(150, settings.WINDOW_HEIGHT - 250, scale=0.40, image=settings.START_IMG, hovered_image=settings.START_IMG_PRESSED)

        # DEFINING TEXT VARIABLES
        heading_text = "Battle Menu"

        # DEFINING CONSTANT VARIABLES
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # DRAWING ON THE SURFACE
        surface.blit(BACKGROUND_IMG)
        utils.render_text(surface, text=heading_text, pos_x=(settings.WINDOW_WIDTH//2), pos_y=100, size=65)
        utils.render_text(surface, text=self.enemytext, pos_x=(settings.WINDOW_WIDTH//2+350), pos_y=250, size=25)
        utils.render_text(surface, text=self.enemy_health, pos_x=(settings.WINDOW_WIDTH//2+350), pos_y=150, size=65)
        surface.blit(self.enemy_image, (settings.WINDOW_WIDTH // 2 + 280, settings.WINDOW_HEIGHT // 2 - 70))

        ## DRAWING BUTTONS ##
        for button in [SURRENDER_BUTTON, FIGHT_BUTTON, DEFENSE_BUTTON, ITEMS_BUTTON, SPELL_BUTTON]:                     # iterate through every single button instance and draw it to the screen
            button.draw(surface)

        if self.FightButtonMenu:
            EMOTIONAL_ATTACK_BUTTON.draw(surface)
            ATTACK_BUTTON.draw(surface)

        ## EVENTS ##
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                                                                               # exit game function
                self.exit_battle()
                self.game.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not self.timer.active and not self.action:
                if SURRENDER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound.play(settings.MENU_SOUND)
                    self.exit_battle()
                if FIGHT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    self.FightButtonMenu = True
                if DEFENSE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    self.defence()
                if ITEMS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    self.current_display = "items_menu"

                if self.FightButtonMenu:
                    if EMOTIONAL_ATTACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.attack_enemy(self.attack_type[1])
                        EMOTIONAL_ATTACK_BUTTON.set_image(settings.START_IMG_PRESSED, scale=0.4)
                    elif ATTACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.attack_enemy(self.attack_type[0])
                        ATTACK_BUTTON.set_image(settings.START_IMG_PRESSED, scale=0.4)

        if self.action:
            if self.action == "Enemy_Fight" and self.enemy_health > 0:
                if self.action_start_time == 0:
                    self.action_start_time = pygame.time.get_ticks()
                elif pygame.time.get_ticks() - self.action_start_time >= self.action_duration:
                    self.attack_player()
                    self.action = None
                    self.action_start_time = 0
            else:
                pass

        self.show_player_health(surface)
        self.show_player_stamina(surface)
        self.show_player_defence(surface)
        if self.show_player_damage_action:
            self.show_player_damage(surface)
        if self.show_enemy_damage_action:
            self.show_enemy_damage(surface)

        if self.enemy_health <= 0:                                                      # if enemy is defeated:
            if self.timer.active == False and not self.timer.is_finished:                         # if timer hasn't been started yet:
                self.timer.start(5000)                                                       # set timer for 'n' ms
            self.timer.update()                                                              # update timer's state
            if self.timer.is_finished:                                                       # if timer is finished
                self.game.player.level += 1                                             # increment player's level
                self.exit_battle()                                                      # exit battle_menu
        else:
            pass
        if self.player_health <= 0:
            self.player_health = 0
            if self.timer.active == False and not self.timer.is_finished:
                self.timer.start(5000)
            self.timer.update()
            if self.timer.is_finished:
                self.exit_battle()
        pygame.display.update()

    def items_menu(self, surface):
        # INITIALIZING BUTTONS
        EXIT_BUTTON = Button(150, settings.WINDOW_HEIGHT - 250, scale=0.40, image=settings.EXIT_IMG, hovered_image=settings.EXIT_IMG_PRESSED)

        # SETTING UP TEXT FOR MENU 
        heading_text = "Your Items"

        # DEFINING CONSTANT VARIABLES
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # DRAWING ON THE SURFACE
        surface.blit(BACKGROUND_IMG)
        utils.render_text(surface, text=heading_text, pos_x=(settings.WINDOW_WIDTH//2), pos_y=(settings.WINDOW_HEIGHT//2-250), size=65)

        ## DRAWING BUTTONS ##
        self.__draw_items(surface, items_pos_init_x=300, items_pos_init_y=200)
        for button in [EXIT_BUTTON]:                     # iterate through every single button instance and draw it to the screen
            button.draw(surface)

        ## EVENTS ##
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                                                                               # exit game function
                self.exit_battle()
                self.game.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EXIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    self.current_display = "battle_menu"
                for item in self.items_dict:
                    if item.checkForInput(MENU_MOUSE_POS):
                        self.use_item(item)
                        self.items_menu_dict_update = True
        pygame.display.update()

    def __draw_items(self, surface, items_pos_init_x, items_pos_init_y, max_length=(settings.WINDOW_WIDTH - 200)):
        items_pos_x = items_pos_init_x
        items_pos_y = items_pos_init_y
        for item in self.game.inventory.items:
            item_name = item.name
            if item.name == "item-test":
                item_image = settings.ITEM_TEST.convert_alpha()
            elif item.name == "item-test2":
                item_image = settings.ITEM_TEST2.convert_alpha()
            button = Button(items_pos_x , items_pos_y, scale=1, image=item_image)
            items_pos_x += 100
            if items_pos_x >= max_length:
                items_pos_y += 100
                items_pos_x = items_pos_init_x
            button.draw(surface)
            if self.items_menu_dict_update:
                item_name = f"{item.name}"
                new_item_info = {button : {'name': item_name}}
                self.items_dict.update(new_item_info)
                self.items_menu_dict_update = False

    def use_item(self, item):
        item_name = str(self.items_dict[item]['name']).strip()
        for item in self.game.inventory.items:
            if item.name == item_name:
                item.use_item()
                self.update_player_data()

    def update_player_data(self):
        change_player_data(health=self.player_health, stamina=self.player_stamina, damage=self.player_damage, defence=self.player_defence)

    def exit_battle(self):
        self.game.player.health = self.player_health
        self.game.npc_enemy.health = self.enemy_health
        self.update_player_data()
        self.is_running = False
