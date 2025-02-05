######### IMPORT ##############
import pygame
from pygame.midi import Input
from settings import *
from pytmx.util_pygame import load_pygame
from entities import *
from sprites import Sprite, BorderSprite, CollidableSprite, TransitionSprite
from groups import *
from dialog import *
from menu import *
from inventory import *
from hud import *
from items import *
from gamedata import *
from input import *
from timer import Timer
from music import Music

import cProfile

######### CLASSES #############

class Game:
    def __init__(self):
        # INITIALIZE FRAMEWORK
        pygame.init()                                                                                                   # initialize pygame framework
        pygame.font.init()                                                                                              # initialize pygame text/font framework

        # INITIALIZE VARIABLES
        self.running = True
        self.action = None                                                                                           # declare/initialize self.action variable that has a default value: False
        self.timer = Timer()
        self.menu = Menu(self)
        self.input = UserInput(self)
        self.inventory = Inventory(self)
        self.music = Music()
        self.time = 0
        self.pressed_start_time = 0
        self.pressed_duration = 5000
        self.music_paused = False

        # CONFIGURING PYGAME
        SCREEN_FLAGS = pygame.HWSURFACE | pygame.DOUBLEBUF
        self.SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), SCREEN_FLAGS)                                            # create screen with (x,y) (tuple)
        pygame.display.set_caption("School-Game-Project(11. Grade)")                                                    # set/change title (caption) of the window
        self.clock = pygame.time.Clock()                                                                                # create a clock
        self.ticks = pygame.time.get_ticks()                                                                            # get ticks (needed in order to count how much time is gone)

        # INTERACTION SETTINGS
        self.action_start_time = 0                                                                                    # interaction start time variable
        self.action_duration = 5000                                                                                   # duration of interaction with NPC variable

        # GROUPS
        self.all_sprites = AllSprites()                                                                                 # create a sprite group # assigns to AllSprites() Class
        self.collision_sprites = pygame.sprite.Group()
        self.transition_sprites = pygame.sprite.Group()

        self.transition_target = 0

        self.import_assets()                                                                                            # import tilesets (assets)
        self.setup(self.tmx_maps['world'], 'spawn')                                                                     # import this one specific tileset (mapset/asset)

        # OTHER VARIABLES
        self.hud = HUD(self.player)

    def import_assets(self):
        self.tmx_maps = {'world': load_pygame(os.path.join('..', 'data', 'maps', 'world.tmx')),                         # load world.tmx file (with given location of it)
                         'world2': load_pygame(os.path.join('..', 'data', 'maps', 'world2.tmx')),
                         'school-building-bottom-left': load_pygame(os.path.join('..', 'data', 'maps', 'school-building-bottom-left.tmx'))}

    def setup(self, tmx_map, player_start_pos):
        # clear the map
        for group in (self.all_sprites, self.collision_sprites, self.transition_sprites):
            group.empty()

        self.static_layer = self.create_static_layer(tmx_map=tmx_map, layer_name='Terrain')

        # GET ENTITIES' POSITION
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player' and obj.properties['pos'] == player_start_pos:                                      # check whether the object's name is Player and its properties for pos(position). Check also whether it is the same as player_start_pos
                if Player.initiated:
                    self.player.teleport((obj.x, obj.y))
                    self.all_sprites.add(self.player)
                    #print("OLD PLAYER")
                else:
                    self.player = Player(self.input, (obj.x, obj.y), self.all_sprites, self.collision_sprites)
                    #print("NEW PLAYER")
            if obj.name == 'Character' and obj.properties['pos'] == 'mid-left':
                if obj.properties['enemy'] == False:
                    self.npc = NPC((obj.x, obj.y), self.all_sprites, game=self)
                if obj.properties['enemy'] == True:
                    self.npc_enemy = NPC_Enemy((obj.x, obj.y), self.all_sprites, game=self)
        # GET ITEMS' POSITION
        for obj in tmx_map.get_layer_by_name('Items'):
            if obj.name == 'Item' and obj.properties['item-name'] == 'item-test':
                self.item_test = Items((obj.x, obj.y), obj.properties['item-name'], self.all_sprites, rarity="RARE",  game=self)
            if obj.name == 'Item' and obj.properties['item-name'] == 'item-test2':
                self.item_test2 = Items((obj.x, obj.y), obj.properties['item-name'], self.all_sprites, rarity="EPIC", game=self)
        # GET OBJECTS' POSITION
        for obj in tmx_map.get_layer_by_name('Objects'):
            CollidableSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        # GET COLLISION OBJECTS' POSITION
        for obj in tmx_map.get_layer_by_name('Collisions'):
            BorderSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)
        # GET TRANSITION OBJECTS' POSITION
        for obj in tmx_map.get_layer_by_name('Transitions'):
            TransitionSprite((obj.x, obj.y), (obj.width, obj.height), (obj.properties['target'], obj.properties['pos']), self.transition_sprites)

    def create_static_layer(self, tmx_map, layer_name):
        layer = pygame.Surface((tmx_map.width * TILE_SIZE, tmx_map.height * TILE_SIZE), pygame.SRCALPHA)
        for x, y, surf in tmx_map.get_layer_by_name(layer_name).tiles():
            layer.blit(surf, (x * TILE_SIZE, y * TILE_SIZE))
        return layer

    # MENU LOGIC
    def menu_logic(self):
        self.menu.show(self.SCREEN)                                                                                     # show menu
        if self.menu.exit_action:
            self.running = False

    # GET PRESSED KEYS
    def menu_get_pressed_keys(self, action):
        if self.input.menu_input(action) == None:
            self.input.menu_input(action)
        else:
            self.menu.get_pressed_keys_action = self.input.menu_input(action)

    def get_random_interact_text(self, data):
        random_number = random.randint(0, len(data) - 1)
        self.random_interact_text = data[random_number]
        return f"{self.random_interact_text}"

    def transition_check(self):
        sprites = [sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox)]
        if sprites:
            self.transition_target = sprites[0].target
            self.setup(self.tmx_maps[self.transition_target[0]], self.transition_target[1])                                                   # import this one specific tileset (mapset/asset)

    # MAIN (RUN) LOGIC
    def run(self):
        # VARIABLES
        self.running = True                                                                                             # initializing variable for main loop
        self.menu_startup = True
        # PYGAME EVENTS
        while self.running == True:
            for event in pygame.event.get():                                                                            # for every single event that is available in pygame do following:
                if event.type == pygame.QUIT:                                                                           # if event type is 'QUIT' do following:
                    self.running = False                                                                                    # quit/exit by assigning boolean 'False' to self.run variable

            dt = self.clock.tick() / 1000                                                                               # tick every second  # dt = difference between previous and next frame
            self.input.run()

            if self.menu_startup == True:
                self.menu_logic()
                self.menu_startup = False

            # PYGAME LOGIC

            self.transition_check()                                                                                     # check if the player is colliding with transition point (TP)
            self.all_sprites.update(dt)                                                                                 # update screen (all sprites) by FPS
            self.SCREEN.fill((173, 216, 230))
            self.SCREEN.blit(self.static_layer, (-(self.player.rect.center[0] - WINDOW_WIDTH / 2), -(self.player.rect.center[1] - WINDOW_HEIGHT / 2)))
            self.all_sprites.draw(self.player.rect.center)                                                              # draw all sprites to the center of the rectangle of the player (camera)
            self.hud.draw(self.SCREEN)

            music_status = self.music.check_status()
            if music_status == "Paused" and self.music.paused == True:
                self.music.unpause()
            elif music_status == "Stopped":
                #self.music.play(MAIN_MUSIC)
                self.music.play_random()
            else:
                pass

            # INTERACTION/ACTION HANDLING
            if self.action:                                                                                   # check whether interact condition is true or not (bool check)
                if self.action == "item_pickup":
                    for item in [self.item_test, self.item_test2]:
                        item.pickup_logic(self.player.rect.center)
                elif self.action == "npc":
                    if self.timer.active == False and not self.timer.is_finished:
                        self.timer.start(self.action_duration)
                        self.get_random_interact_text(NPC_INTERACT_DATA)
                    if self.timer.is_finished:
                        self.action = None
                        self.timer.is_finished = False
                    self.timer.update()
                    self.npc.interact(self.random_interact_text, self.player.rect)
                elif self.action == "npc_enemy":
                    self.npc_enemy.interact(self.SCREEN, self.player.rect)

            #for npc in [self.npc, self.npc_enemy]:
            try:
                self.npc.interactInRange(self.SCREEN)
            except AttributeError:
                pass
            try:
                self.npc_enemy.interactInRange(self.SCREEN)
            except AttributeError:
                pass



            ## GET CURRENT FPS ##
            #print(self.clock.get_fps())

            pygame.display.flip()                                                                                     # refresh(update) the screen


####### MAIN CODE ############

if __name__ == "__main__":                                                                                              # if code is in main.py (__main__) run following
    game = Game()                                                                                                       # initialize game() (class)
    game.run()                                                                                                          # run game (game-logic)

    ## DEBUG ##
    #cProfile.run('game.run()')
