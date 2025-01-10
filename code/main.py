######### IMPORT ##############
import pygame
from pygame.midi import Input

from settings import *
from pytmx.util_pygame import load_pygame
from entities import *
from sprites import Sprite
from groups import *
from dialog import *
from menu import *
from inventory import *
from hud import *
from items import *
from gamedata import *
from input import *

######### CLASSES #############

class Game:
    def __init__(self):
        # INITIALIZE FRAMEWORK
        pygame.init()                                                                                                   # initialize pygame framework
        pygame.font.init()                                                                                              # initialize pygame text/font framework

        # INITIALIZE VARIABLES
        self.running = True
        self.interact = False                                                                                           # declare/initialize self.interact variable that has a default value: False
        self.menu = Menu(self)
        self.items = Items(self)
        self.input = UserInput(self)
        self.inventory = Inventory(self)
        self.hud = HUD()
        self.time = 0
        self.pressed_start_time = 0
        self.pressed_duration = 5000


        # CONFIGURING PYGAME
        self.SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))                                            # create screen with (x,y) (tuple)
        pygame.display.set_caption("School-Game-Project(11. Grade)")                                                    # set/change title (caption) of the window
        self.clock = pygame.time.Clock()                                                                                # create a clock
        self.ticks = pygame.time.get_ticks()                                                                            # get ticks (needed in order to count how much time is gone)

        # INTERACTION SETTINGS
        self.interact_start_time = 0                                                                                    # interaction start time variable
        self.interact_duration = 5000                                                                                   # duration of interaction with NPC variable


        # GROUPS
        self.all_sprites = AllSprites()                                                                                 # create a sprite group # assigns to AllSprites() Class

        self.import_assets()                                                                                            # import tilesets (assets)
        self.setup(self.tmx_maps['world'], 'spawn')                                                                     # import this one specific tileset (mapset/asset)
        
    def import_assets(self):
        self.tmx_maps = {'world': load_pygame(os.path.join('..', 'data', 'maps', 'world.tmx'))}                         # load world.tmx file (with given location of it)
        
    def setup(self, tmx_map, player_start_pos):
        for x,y, surf in tmx_map.get_layer_by_name('Terrain').tiles():                                                  # get only 'Terrain' layer from world.tmx
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)                                              # parse information of sprite to Sprite() class
        # GET ENTITIES' POSITION
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player' and obj.properties['pos'] == player_start_pos:                                      # check whether the object's name is Player and its properties for pos(position). Check also whether it is the same as player_start_pos
                self.player = Player((obj.x, obj.y), self.all_sprites)                                                  # create player() instance with object's x and y coordinates that we got from tilemap(tmx). And assign player() instance to AllSprites() group/class
            if obj.name == 'Character' and obj.properties['pos'] == 'bottom-right':
                self.npc = NPC((obj.x, obj.y), self.all_sprites)
        # GET ITEMS' POSITION
        for obj in tmx_map.get_layer_by_name('Items'):
            if obj.name == 'Item' and obj.properties['item-name'] == 'item-test':
                #self.items = Items((obj.x, obj.y), obj.properties['item-name'], self.all_sprites)                       # obj.properties['item-name'] gets the name of item's name and puts it into Items() Class
                self.items.add((obj.x, obj.y), obj.properties['item-name'])
            if obj.name == 'Item' and obj.properties['item-name'] == 'item-test2':
                #self.items = Items((obj.x, obj.y), obj.properties['item-name'], self.all_sprites)                       # obj.properties['item-name'] gets the name of item's name and puts it into Items() Class
                self.items.add((obj.x, obj.y), obj.properties['item-name'])

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


    def get_random_interact_text(self):
        random_number = random.randint(0, len(NPC_INTERACT_DATA) - 1)
        self.random_interact_text = NPC_INTERACT_DATA[random_number]

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


            self.input.run()

            if self.menu_startup == True:
                self.menu_logic()
                self.menu_startup = False

            # PYGAME LOGIC
            dt = self.clock.tick() / 1000                                                                               # tick every second  # dt = difference between previous and next frame
            self.all_sprites.update(dt)                                                                                 # update screen (all sprites) by FPS
            self.SCREEN.fill('white')                                                                                   # fill screen with white color, so it's fully updated
            self.all_sprites.draw(self.player.rect.center)                                                              # draw all sprites to the center of the rectangle of the player (camera)
            self.items.draw(self.SCREEN, self.player.rect.center)
            self.hud.draw(self.SCREEN)

            # INTERACTION HANDLING
            if self.interact == True:                                                                                   # check whether interact condition is true or not (bool check)
                if self.interact_start_time == 0:                                                                       # if interact start time equals to 0, do following:
                    self.interact_start_time = pygame.time.get_ticks()                                                  # assign ticks to interact start time variable
                    self.get_random_interact_text()
                elif pygame.time.get_ticks() - self.interact_start_time >= self.interact_duration:                      # else if more or equal time than interact duration has been gone do following:
                    self.interact = False                                                                               # turn interaction off
                    self.interact_start_time = 0                                                                        # reset interact start time counter

                self.npc.interact(self.random_interact_text, self.player.rect)

            else:                                                                                                       # else (interact isn't true)
                self.interact_start_time = 0                                                                            # reset interact start time

            pygame.display.update()                                                                                     # refresh(update) the screen


####### MAIN CODE ############

if __name__ == "__main__":                                                                                              # if code is in main.py (__main__) run following
    game = Game()                                                                                                       # initialize game() (class)
    game.run()                                                                                                          # run game (game-logic)
