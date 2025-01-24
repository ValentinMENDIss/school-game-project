######### IMPORT ##############

import pygame

from settings import *
from gamedata import NPC_ENEMY_INTERACT_DATA 
from button import Button

######### SPRITES ##############

BACKGROUND_IMG = pygame.image.load(os.path.join('..', 'graphics', 'battle-menu-background.png'))

######### CLASSes ##############

class Battle_Menu:
    def __init__(self):
        self.get_pressed_keys_action = False
        self.exit_action = False
        # TEXTs
        self.enemytext = "test"

    def random_text(self):
        if self.enemy_health <= 0:
            self.enemytext = "Congratulations, You've won me..."
        else:
            index = random.randint(0, len(NPC_ENEMY_INTERACT_DATA) - 1)
            self.enemytext = NPC_ENEMY_INTERACT_DATA[index]

    def attack_enemy(self, attack_type):
        if attack_type == "emotional_attack":
            self.enemy_health -= random.randint(0, 15) 
            self.random_text()
        elif attack_type == "attack":
            self.enemy_health -= random.randint(0, 25)
            self.random_text()

    # DRAWING LOGIC
    def draw(self, surface, enemy_health):
        self.enemy_health = enemy_health
        running = True
        FightButtonMenu = None
        while running:
            # DEFINING CONSTANT VARIABLES
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            # SETTING TEXT FOR MENU
            heading_text = "Battle Menu"

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

            ## INITIALIZING BUTTONS AND DRAWING THEM ##
            SURRENDER_BUTTON = Button(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 100, SURRENDER_IMG, 0.40)                             # create button instance
            FIGHT_BUTTON = Button(150, WINDOW_HEIGHT - 100, START_IMG, 0.40)
            DEFENSE_BUTTON = Button(400, WINDOW_HEIGHT - 100, START_IMG, 0.40)
            ITEMS_BUTTON = Button(650, WINDOW_HEIGHT - 100, START_IMG, 0.40)
            SPELL_BUTTON = Button(900, WINDOW_HEIGHT - 100, START_IMG, 0.40)

            for button in [SURRENDER_BUTTON, FIGHT_BUTTON, DEFENSE_BUTTON, ITEMS_BUTTON, SPELL_BUTTON]:                     # iterate through every single button instance and draw it to the screen
                button.draw(surface)

            EMOTIONAL_ATTACK_BUTTON = Button(150, WINDOW_HEIGHT - 175, START_IMG, 0.40)
            ATTACK_BUTTON = Button(150, WINDOW_HEIGHT - 250, START_IMG, 0.40)

            if FightButtonMenu:
                EMOTIONAL_ATTACK_BUTTON.draw(surface)
                ATTACK_BUTTON.draw(surface)

            ## EVENTS ##
            for event in pygame.event.get():
                if event.type == pygame.QUIT:                                                                               # exit game function
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if SURRENDER_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.mixer.Sound.play(MENU_SOUND)
                        pygame.mixer.music.stop()
                        running = False
                    if FIGHT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        FightButtonMenu = True
                    if FightButtonMenu:
                        if EMOTIONAL_ATTACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                            self.attack_enemy("emotional_attack")
                            print("EMOTIONAL_ATTACK_BUTTON Pressed") 
                        elif ATTACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                            self.attack_enemy("attack")
                            print("ATTACK_BUTTON Pressed")

            if self.enemy_health <= 0:
                print("You've won me")
            else:
                pass

            print(self.enemy_health)
            pygame.display.update()
            
