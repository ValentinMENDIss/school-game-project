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
        self.game = game
        self.attack_type = ["attack", "emotional_attack"]
        self.get_pressed_keys_action = False
        self.exit_action = False
        self.enemy_health = enemy_health
        self.player_health = 100
        self.damage = 0
        self.show_damage_action = False
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
            self.enemy_dmg = random.randint(0, 25)
            self.enemy_health -= self.enemy_dmg
            self.random_text()
        elif attack_type == "emotional_attack":
            self.enemy_dmg = random.randint(0, 15)
            self.enemy_health -= self.enemy_dmg
            self.random_text()
        self.show_damage_action = True

    # SHOW DEALT DAMAGE ON THE SCREEN
    def show_damage(self, surface):
        size = 25
        DAMAGETEXT = pygame.font.Font(os.path.join('..', 'font', 'Pixeltype.ttf'), size)

        damagetext = DAMAGETEXT.render(str(self.enemy_dmg), True, (210,39,48)).convert_alpha()        # render an enemy text
        damagetextrect = damagetext.get_rect()
        damagetextrect.center = (WINDOW_WIDTH // 2 + 350, WINDOW_HEIGHT // 2 - 50)

        surface.blit(damagetext, damagetextrect)
        if size >= 35:
            self.show_damage_action = False

    def attack_player(self):
        index = random.randint(0, len(self.attack_type) - 1)
        attack_type = self.attack_type[index]

        if attack_type == "attack":
            self.damage = random.randint(0, 25)
            self.player_health -= self.damage
        if attack_type == "emotional_attack":
            self.damage = random.randint(0, 15)
            self.player_health -= self.damage

    # DRAWING LOGIC
    def draw(self, surface):
        FightButtonMenu = None
        # ACTION
        action = None
        action_start_time = 0
        action_duration = 2000
        # LOOP VARIABLES
        running = True

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
       # LOOP
        while running:
            # DEFINING CONSTANT VARIABLES
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            # DEFINING TEXT VARIABLES
            headingtext = HEADINGTEXT.render(heading_text, True, (0, 0, 0)).convert_alpha()  # render a Small Text
            headingtextrect = headingtext.get_rect()                                                              # get a Rectangle of the small Text ( needed, to be able to place the text precisely )
            headingtextrect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 250)                                     # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )

            enemytext = SMALLTEXT.render(self.enemytext, True, (0, 0, 0)).convert_alpha()        # render an enemy text
            enemytextrect = enemytext.get_rect()
            enemytextrect.center = (WINDOW_WIDTH // 2 + 350, WINDOW_HEIGHT // 2)

            # DRAWING ON THE SURFACE
            surface.blit(BACKGROUND_IMG)
            surface.blit(headingtext, headingtextrect)
            surface.blit(enemytext, enemytextrect)

            ## DRAWING BUTTONS ##
            for button in [SURRENDER_BUTTON, FIGHT_BUTTON, DEFENSE_BUTTON, ITEMS_BUTTON, SPELL_BUTTON]:                     # iterate through every single button instance and draw it to the screen
                button.draw(surface)

            if FightButtonMenu:
                EMOTIONAL_ATTACK_BUTTON.draw(surface)
                ATTACK_BUTTON.draw(surface)
            ## EVENTS ##
            for event in pygame.event.get():
                if event.type == pygame.QUIT:                                                                               # exit game function
                    running = False
                    self.game.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and not timer.active:
                    if SURRENDER_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.mixer.Sound.play(MENU_SOUND)
                        pygame.mixer.music.stop()
                        running = False
                        #return False
                    if FIGHT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        FightButtonMenu = True
                    if FightButtonMenu:
                        if EMOTIONAL_ATTACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                            self.attack_enemy(self.attack_type[1])
                            EMOTIONAL_ATTACK_BUTTON.set_image(START_IMG_PRESSED, scale=0.4)
                            print("EMOTIONAL_ATTACK_BUTTON Pressed")
                            action = "Fight"
                        elif ATTACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                            self.attack_enemy(self.attack_type[0])
                            ATTACK_BUTTON.set_image(START_IMG_PRESSED, scale=0.4)
                            print("ATTACK_BUTTON Pressed")
                            action = "Fight"

            if action:
                if action == "Fight":
                    if action_start_time == 0:
                        action_start_time = pygame.time.get_ticks()
                    elif pygame.time.get_ticks() - action_start_time >= action_duration:
                        self.attack_player()
                        print(f"PLAYER HEALTH: {self.player_health}")
                        action = None
                        action_start_time = 0
                else:
                    pass

            if self.show_damage_action:
                self.show_damage(surface)
            if self.enemy_health <= 0:
                print("You've won me")
                if timer.active == False and not timer.is_finished:
                    timer.start(5000)
                timer.update()
                if timer.is_finished:
                    running = False
            else:
                pass

            print(self.enemy_health)
            pygame.display.update()
