######### IMPORT ##############
import pygame

from settings import *
from pytmx.util_pygame import load_pygame
from entities import *
from sprites import Sprite
from groups import *
from dialog import *
from menu import Menu
from inventory import *
from items import *

######### CLASSES #############

class Game:
    def __init__(self):
        # INITIALIZE FRAMEWORK
        pygame.init()                                                                                                   # initialize pygame framework
        pygame.font.init()                                                                                              # initialize pygame text/font framework

        # INITIALIZE VARIABLES
        self.running = True
        self.interact = False                                                                                           # declare/initialize self.interact variable that has a default value: False
        #self.button_value = None                                                                                        # setting button value for gamepad to 0
        self.menu = Menu()

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
        self.items = Items()
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

    #def item_pickup_logic(self, name, pos):

    # GET USER INPUT
    def input(self):
        # KEYBOARD INPUT
        keys = pygame.key.get_just_pressed()                                                                            # initialize new variable(keys) that will get user's input, but the buttons can be detected as pressed and not as hold too.

        # JOYSTICK INPUT
        pygame.joystick.init()


        self.num_joysticks = pygame.joystick.get_count()
        if self.num_joysticks > 0:
            self.my_joystick = pygame.joystick.Joystick(0)
            self.joystick_x_axis = self.my_joystick.get_axis(0)
            self.joystick_y_axis = self.my_joystick.get_axis(1)
            self.joystick_input_vector = (self.joystick_x_axis, self.joystick_y_axis)
            self.button_value = None

            # Reset the joystick input vector if the joystick is not being moved
            if abs(self.joystick_x_axis) < 0.1 and abs(self.joystick_y_axis) < 0.1:
                self.joystick_input_vector = pygame.Vector2(0, 0)

            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    #print(f"Button {event.button} pressed")
                    self.player.input_joystick(button_value=event.button)
                    self.button_value = event.button
                elif event.type == pygame.JOYAXISMOTION:
                    #print(f"Axis {event.axis} moved to {event.value}")
                    self.player.input_joystick(axes_value=(self.joystick_input_vector))


        if keys[pygame.K_e] or (self.num_joysticks > 0 and self.button_value == 0):                                                                                            # if just pressed key is e do following:
            self.items.pickup_logic()

            # DIALOG SYSTEM
            if abs(self.npc.rect[0] - self.player.rect[0]) <= 200 and abs(self.npc.rect[1] - self.player.rect[1]) <= 200: # check npc's and player's position. If the differences between each x and y coordinates are smaller in value than 200 do following:
                pygame.mixer.Sound.play(YIPPEE_SOUND)
                pygame.mixer.music.stop()
                self.interact = True                                                                                    # assign following value to self.interact variable: True

        if keys[pygame.K_ESCAPE]:
            self.menu_logic()


    def menu_logic(self):
        self.menu.show(self.SCREEN)
        if self.menu.exit_action:
            self.running = False

    def run(self):
        # VARIABLES
        self.running = True                                                                                                 # initializing variable for main loop

        self.menu_logic()                                                                                               # calling menu logic

        # PYGAME EVENTS
        while self.running == True:
            for event in pygame.event.get():                                                                            # for every single event that is available in pygame do following:
                if event.type == pygame.QUIT:                                                                           # if event type is 'QUIT' do following:
                    self.running = False                                                                                    # quit/exit by assigning boolean 'False' to self.run variable


            # PYGAME LOGIC
            dt = self.clock.tick() / 1000                                                                               # tick every second  # dt = difference between previous and next frame
            self.all_sprites.update(dt)                                                                                 # update screen (all sprites) by FPS
            self.SCREEN.fill('white')                                                                                   # fill screen with white color, so it's fully updated
            self.all_sprites.draw(self.player.rect.center)                                                              # draw all sprites to the center of the rectangle of the player (camera)
            self.items.draw(self.SCREEN, self.player.rect.center)
            self.input()

            # INTERACTION HANDLING
            if self.interact == True:                                                                                   # check whether interact condition is true or not (bool check)
                self.npc.interact("OMG, I CAN SPEAK!!! Thank you developers :3"
                                  "\nOh... also try to get near these Items and to press E. See what happens :3", self.player.rect)                      # interact with npc, text in speech bubble
                if self.interact_start_time == 0:                                                                       # if interact start time equals to 0, do following:
                    self.interact_start_time = pygame.time.get_ticks()                                                  # assign ticks to interact start time variable
                elif pygame.time.get_ticks() - self.interact_start_time >= self.interact_duration:                      # else if more or equal time than interact duration has been gone do following:
                    self.interact = False                                                                               # turn interaction off
                    self.interact_start_time = 0                                                                        # reset interact start time counter
            else:                                                                                                       # else (interact isn't true)
                self.interact_start_time = 0                                                                            # reset interact start time

            pygame.display.update()                                                                                     # refresh(update) the screen


####### MAIN CODE ############

if __name__ == "__main__":                                                                                              # if code is in main.py (__main__) run following
    game = Game()                                                                                                       # initialize game() (class)
    game.run()                                                                                                          # run game (game-logic)