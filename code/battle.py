######### IMPORT ##############

import pygame
from random import randint

from settings import *
from gamedata import NPC_ENEMY_INTERACT_DATA
from button import Button
from timer import Timer

######### SPRITES ##############

BACKGROUND_IMG = pygame.image.load(os.path.join('..', 'graphics', 'battle-menu-background.png'))

######### CLASSes ##############

class Battle_Menu:
    def __init__(self, enemy_health, game):
        self.game = game                                                                                                                    # declare new variable that stores main.py (Game()) loop's attributes and variables
        self.attack_type = ["attack", "emotional_attack"]                                                                                   # declare attack types
        self.get_pressed_keys_action = False                                                                                                # variable that stores Bool value. Checks if action should be called
        self.exit_action = False                                                                                                            # variable that stores Bool value. Checks if action should be called
        self.show_player_damage_action = False                                                                                              # variable that stores Bool value. Checks if action should be called
        self.show_enemy_damage_action = False                                                                                               # variable that stores Bool value. Checks if action should be called
        self.enemy_health = enemy_health                                                                                                    # enemy's health
        self.player_health = 100                                                                                                            # player's health
        self.damage = 0                                                                                                                     # variable that stores dealt damage in one round
        # IMAGES
        self.enemy_image = NPC_IDLE.convert_alpha()
        self.enemy_new_size_image = (self.enemy_image.get_width() * 4, self.enemy_image.get_height() * 4)                                 # declare new variable that has 4 times bigger scale than the player's image
        self.enemy_image = (pygame.transform.scale(self.enemy_image, self.enemy_new_size_image))
        # TEXTs
        self.enemytext = ""
        self.damagetext = ""

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
        FightButtonMenu = None
        # ACTION
        action = None
        action_start_time = 0
        action_duration = 2000
        # LOOP VARIABLES
        self.running = True

        # INITALIZING BUTTONS
        SURRENDER_BUTTON = Button(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 100, scale=0.40, image=SURRENDER_IMG, hovered_image=SURRENDER_IMG_PRESSED)                             # create button instance
        FIGHT_BUTTON = Button(150, WINDOW_HEIGHT - 100, scale=0.40, image=START_IMG, hovered_image=START_IMG_PRESSED)
        DEFENSE_BUTTON = Button(400, WINDOW_HEIGHT - 100, scale=0.40, image=START_IMG, hovered_image=START_IMG_PRESSED)
        ITEMS_BUTTON = Button(650, WINDOW_HEIGHT - 100, scale=0.40, image=START_IMG, hovered_image=START_IMG_PRESSED)
        SPELL_BUTTON = Button(900, WINDOW_HEIGHT - 100, scale=0.40, image=START_IMG, hovered_image=START_IMG_PRESSED)

        EMOTIONAL_ATTACK_BUTTON = Button(150, WINDOW_HEIGHT - 175, scale=0.40, image=START_IMG, hovered_image=START_IMG_PRESSED)
        ATTACK_BUTTON = Button(150, WINDOW_HEIGHT - 250, scale=0.40, image=START_IMG, hovered_image=START_IMG_PRESSED)

        # SETTING TEXT FOR MENU
        heading_text = "Battle Menu"
        timer = Timer()
        self.game.music.pause()
       # LOOP
        while self.running:
            # DEFINING CONSTANT VARIABLES
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            # DEFINING TEXT VARIABLES
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

            if FightButtonMenu:
                EMOTIONAL_ATTACK_BUTTON.draw(surface)
                ATTACK_BUTTON.draw(surface)
            ## EVENTS ##
            for event in pygame.event.get():
                if event.type == pygame.QUIT:                                                                               # exit game function
                    self.exit_battle()
                    self.game.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and not timer.active and not action:
                    if SURRENDER_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.mixer.Sound.play(MENU_SOUND)
                        self.exit_battle()
                    if FIGHT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        FightButtonMenu = True
                    if FightButtonMenu:
                        if EMOTIONAL_ATTACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                            self.attack_enemy(self.attack_type[1])
                            EMOTIONAL_ATTACK_BUTTON.set_image(START_IMG_PRESSED, scale=0.4)
                            action = "Enemy_Fight"                                                                          # after player's fight, set action variable that corresponds to fight for NPC_ENEMY
                        elif ATTACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                            self.attack_enemy(self.attack_type[0])
                            ATTACK_BUTTON.set_image(START_IMG_PRESSED, scale=0.4)
                            action = "Enemy_Fight"                                                                          # after player's fight, set action variable that corresponds to fight for NPC_ENEMY

            if action:
                if action == "Enemy_Fight" and self.enemy_health > 0:
                    if action_start_time == 0:
                        action_start_time = pygame.time.get_ticks()
                    elif pygame.time.get_ticks() - action_start_time >= action_duration:
                        self.attack_player()
                        action = None
                        action_start_time = 0
                else:
                    pass

            if self.show_player_damage_action:
                self.show_player_damage(surface)
            if self.show_enemy_damage_action:
                self.show_enemy_damage(surface)

            if self.enemy_health <= 0:
                print("You've won me")
                if timer.active == False and not timer.is_finished:
                    timer.start(5000)
                timer.update()
                if timer.is_finished:
                    self.exit_battle()
            else:
                pass

            if self.player_health <= 0:
                self.player_health = 0
                print("I've won you!")
                if timer.active == False and not timer.is_finished:
                    timer.start(5000)
                timer.update()
                if timer.is_finished:
                    self.exit_battle()

            pygame.display.update()

    def exit_battle(self):
        self.running = False
