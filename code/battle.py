######### IMPORT ##############

import pygame
from random import randint

from settings import *
from gamedata import NPC_ENEMY_INTERACT_DATA
from button import Button
from timer import Timer
from savedata import load_saved_data

######### SPRITES ##############

BACKGROUND_IMG = pygame.image.load(os.path.join('..', 'graphics', 'background', 'battle-menu-background.png'))

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
        self.player_data = load_saved_data()
        self.player_health = self.player_data['health']                                                                                        # player's health
        
        self.damage = 0                                                                                                                     # variable that stores dealt damage in one round
        self.is_running = True
        self.FightButtonMenu = False
        # ACTION
        self.action = None
        self.action_start_time = 0
        self.action_duration = 2000
        # IMAGES
        self.enemy_image = NPC_IDLE.convert_alpha()
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
        if attack_type == "attack":
            self.player_damage = random.randint(0, 25)
            self.enemy_health -= self.player_damage
            self.random_text()
        elif attack_type == "emotional_attack":
            self.player_damage = random.randint(0, 15)
            self.enemy_health -= self.player_damage
            self.random_text()
        self.show_player_damage_action = True

    # SHOW DEALT DAMAGE ON THE SCREEN
    def show_player_damage(self, surface):
        size = 25
        DAMAGETEXT = pygame.font.Font(os.path.join('..', 'font', 'Pixeltype.ttf'), size)

        damagetext = DAMAGETEXT.render(str(self.player_damage), True, (210,39,48)).convert_alpha()        # render an enemy text
        damagetextrect = damagetext.get_rect()
        damagetextrect.center = (WINDOW_WIDTH // 2 + 350, WINDOW_HEIGHT // 2 - 150)

        surface.blit(damagetext, damagetextrect)
#        if size >= 35:
#            self.show_damage_action = False

    def show_enemy_damage(self, surface):
        size = 25
        DAMAGETEXT = pygame.font.Font(os.path.join('..', 'font', 'Pixeltype.ttf'), size)

        damagetext = DAMAGETEXT.render(str(self.enemy_damage), True, (210,39,48)).convert_alpha()        # render an enemy text
        damagetextrect = damagetext.get_rect()
        damagetextrect.center = (450, 450)

        surface.blit(damagetext, damagetextrect)

    def attack_player(self):
        index = random.randint(0, len(self.attack_type) - 1)
        attack_type = self.attack_type[index]
        if attack_type == "attack":
            self.enemy_damage = random.randint(0, 25)
            self.player_health -= self.enemy_damage
        if attack_type == "emotional_attack":
            self.enemy_damage = random.randint(0, 15)
            self.player_health -= self.enemy_damage
        self.show_enemy_damage_action = True

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
        SURRENDER_BUTTON = Button(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 100, scale=0.40, image=SURRENDER_IMG, hovered_image=SURRENDER_IMG_PRESSED)                             # create button instance
        FIGHT_BUTTON = Button(150, WINDOW_HEIGHT - 100, scale=0.40, image=START_IMG, hovered_image=START_IMG_PRESSED)
        DEFENSE_BUTTON = Button(400, WINDOW_HEIGHT - 100, scale=0.40, image=START_IMG, hovered_image=START_IMG_PRESSED)
        ITEMS_BUTTON = Button(650, WINDOW_HEIGHT - 100, scale=0.40, image=START_IMG, hovered_image=START_IMG_PRESSED)
        SPELL_BUTTON = Button(900, WINDOW_HEIGHT - 100, scale=0.40, image=START_IMG, hovered_image=START_IMG_PRESSED)
        EMOTIONAL_ATTACK_BUTTON = Button(150, WINDOW_HEIGHT - 175, scale=0.40, image=START_IMG, hovered_image=START_IMG_PRESSED)
        ATTACK_BUTTON = Button(150, WINDOW_HEIGHT - 250, scale=0.40, image=START_IMG, hovered_image=START_IMG_PRESSED)

        # DEFINING TEXT VARIABLES
        heading_text = "Battle Menu"

        headingtext = HEADINGTEXT.render(heading_text, True, (0, 0, 0)).convert_alpha()  # render a Small Text
        headingtextrect = headingtext.get_rect()                                                              # get a Rectangle of the small Text ( needed, to be able to place the text precisely )
        headingtextrect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 250)                                     # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )

        enemytext = SMALLTEXT.render(self.enemytext, True, (0, 0, 0)).convert_alpha()        # render an enemy text
        enemytextrect = enemytext.get_rect()
        enemytextrect.center = (WINDOW_WIDTH // 2 + 350, WINDOW_HEIGHT // 2 - 100)

        playerhealthtext = HEADINGTEXT.render(str(self.player_health), True, (4,106,56)).convert_alpha()        # render an enemy text
        playerhealthtextrect = playerhealthtext.get_rect()
        playerhealthtextrect.center = (450, 500)

        enemyhealthtext = HEADINGTEXT.render(str(self.enemy_health), True, (4,106,56)).convert_alpha()        # render an enemy text
        enemyhealthtextrect = enemyhealthtext.get_rect()
        enemyhealthtextrect.center = (WINDOW_WIDTH // 2 + 350, 150)

        # DEFINING CONSTANT VARIABLES
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # DRAWING ON THE SURFACE
        surface.blit(BACKGROUND_IMG)
        surface.blit(headingtext, headingtextrect)
        surface.blit(enemytext, enemytextrect)
        surface.blit(playerhealthtext, playerhealthtextrect)
        surface.blit(enemyhealthtext, enemyhealthtextrect)
        surface.blit(self.enemy_image, (WINDOW_WIDTH // 2 + 280, WINDOW_HEIGHT // 2 - 70))

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
                    pygame.mixer.Sound.play(MENU_SOUND)
                    self.exit_battle()
                if ITEMS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    self.current_display = "items_menu"
                if FIGHT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    self.FightButtonMenu = True

                if self.FightButtonMenu:
                    if EMOTIONAL_ATTACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.attack_enemy(self.attack_type[1])
                        EMOTIONAL_ATTACK_BUTTON.set_image(START_IMG_PRESSED, scale=0.4)
                        self.action = "Enemy_Fight"                                                                          # after player's fight, set action variable that corresponds to fight for NPC_ENEMY
                    elif ATTACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.attack_enemy(self.attack_type[0])
                        ATTACK_BUTTON.set_image(START_IMG_PRESSED, scale=0.4)
                        self.action = "Enemy_Fight"                                                                          # after player's fight, set action variable that corresponds to fight for NPC_ENEMY

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
        EXIT_BUTTON = Button(150, WINDOW_HEIGHT - 250, scale=0.40, image=EXIT_IMG, hovered_image=EXIT_IMG_PRESSED)

        # SETTING TEXT FOR MENU
        heading_text = "Your Items"

        # DEFINING TEXT VARIABLES
        headingtext = HEADINGTEXT.render(heading_text, True, (0, 0, 0)).convert_alpha()  # render a Small Text
        headingtextrect = headingtext.get_rect()                                                              # get a Rectangle of the small Text ( needed, to be able to place the text precisely )
        headingtextrect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 250)                                     # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )

        # DEFINING CONSTANT VARIABLES
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # DRAWING ON THE SURFACE
        surface.blit(BACKGROUND_IMG)
        surface.blit(headingtext, headingtextrect)

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

    def __draw_items(self, surface, items_pos_init_x, items_pos_init_y, max_length=(WINDOW_WIDTH - 200)):
        items_pos_x = items_pos_init_x
        items_pos_y = items_pos_init_y
        for item in self.game.inventory.items:
            item_name = item.name
            if item.name == "item-test":
                item_image = ITEM_TEST.convert_alpha()
            elif item.name == "item-test2":
                item_image = ITEM_TEST2.convert_alpha()
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
                self.update_player_health()
                
    def update_player_health(self):
        self.player_data = load_saved_data()
        self.player_health = self.player_data['health']

    def exit_battle(self):
        self.game.player.health = self.player_health
        self.game.npc_enemy.health = self.enemy_health
        self.is_running = False
