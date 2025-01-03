######### IMPORT ##############
from settings import *
from pytmx.util_pygame import load_pygame
from entities import *
from sprites import Sprite
from groups import *
from dialog import *
from button import *

######### CLASSES #############

class Game:
    def __init__(self):
        # INITIALIZE FRAMEWORK
        pygame.init()                                                                                                   # initialize pygame framework
        pygame.font.init()                                                                                              # initialize pygame text/font framework

        # INITIALIZE VARIABLES
        self.running = True
        self.interact = False                                                                                           # declare/initialize self.interact variable that has a default value: False

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

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player' and obj.properties['pos'] == player_start_pos:                                      # check whether the object's name is Player and its properties for pos(position). Check also whether it is the same as player_start_pos
                self.player = Player((obj.x, obj.y), self.all_sprites)                                                  # create player() instance with object's x and y coordinates that we got from tilemap(tmx). And assign player() instance to AllSprites() group/class
            if obj.name == 'Character' and obj.properties['pos'] == 'bottom-right':
                self.npc = NPC((obj.x, obj.y), self.all_sprites)
<<<<<<< HEAD
=======
        # GET ITEMS' POSITION
        for obj in tmx_map.get_layer_by_name('Items'):
            if obj.name == 'Item' and obj.properties['item-name'] == 'item-test':
                self.items = Items((obj.x, obj.y), obj.properties['item-name'], self.all_sprites)                       # obj.properties['item-name'] gets the name of item's name and puts it into Items() Class
            if obj.name == 'Item' and obj.properties['item-name'] == 'item-test2':
                self.items = Items((obj.x, obj.y), obj.properties['item-name'], self.all_sprites)                       # obj.properties['item-name'] gets the name of item's name and puts it into Items() Class

    #def item_pickup_logic(self, name, pos):

>>>>>>> fa1053c (added not fully implemented yet Item pickup logic)

    # DIALOG SYSTEM
    def input(self):
        keys = pygame.key.get_just_pressed()                                                                            # initialize new variable(keys) that will get user's input, but the buttons can be detected as pressed and not as hold too.
        if keys[pygame.K_e]:                                                                                            # if just pressed key is e do following:

            ### TESTING ####
            self.items.get_position()

            ################

            if abs(self.npc.rect[0] - self.player.rect[0]) <= 200 and abs(self.npc.rect[1] - self.player.rect[1]) <= 200: # check npc's and player's position. If the differences between each x and y coordinates are smaller in value than 200 do following:
<<<<<<< HEAD
=======
                pygame.mixer.Sound.play(YIPPEE_SOUND)
                pygame.mixer.music.stop()
>>>>>>> a6084fb (Added Exit Button to the Main Menu)
                self.interact = True                                                                                    # assign following value to self.interact variable: True
<<<<<<< HEAD
=======
            #elif abs(self.items. - self.player.rect[0]) <= 50 and abs(self.items.pos[1] - self.player.rect[1]) <= 50:                                                                                 # ; [0] = x; [1] = y;
                  # here I will need to so that the self.item will delete the item that is near the player and paste into user's inventory
                     # but for that I will need to rework items completely. I will need to create a dictionary where I will save an x and y position for the item, as well as a name of the item itself.

        if keys[pygame.K_ESCAPE]:
            self.menu_logic()
>>>>>>> fa1053c (added not fully implemented yet Item pickup logic)


<<<<<<< HEAD
=======
    def menu_logic(self):
        self.menu.show(self.SCREEN)
        if self.menu.exit_action:
            self.running = False

>>>>>>> a6084fb (Added Exit Button to the Main Menu)
    def run(self):
        # VARIABLES
        self.running = True                                                                                                 # initializing variable for main loop

<<<<<<< HEAD
=======
        self.menu_logic()                                                                                               # calling menu logic

>>>>>>> a6084fb (Added Exit Button to the Main Menu)
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
            self.input()                                                                                                # take user's input

            # INTERACTION HANDLING
            if self.interact == True:                                                                                   # check whether interact condition is true or not (bool check)
                self.npc.interact("OMG, I CAN SPEAK!!! Thank you developers :3", self.player.rect)                      # interact with npc, text in speech bubble
                if self.interact_start_time == 0:                                                                       # if interact start time equals to 0, do following:
                    self.interact_start_time = pygame.time.get_ticks()                                                  # assign ticks to interact start time variable
                elif pygame.time.get_ticks() - self.interact_start_time >= self.interact_duration:                      # else if more or equal time than interact duration has been gone do following:
                    self.interact = False                                                                               # turn interaction off
                    self.interact_start_time = 0                                                                        # reset interact start time counter
            else:                                                                                                       # else (interact isn't true)
                self.interact_start_time = 0                                                                            # reset interact start time



            ### TESTING ###
            self.start_button = Button(100,200,START_IMG, 0.8)		#create button instance
            self.start_button.draw(self.SCREEN)

            pygame.display.update()                                                                                     # refresh(update) the screen

####### MAIN CODE ############

if __name__ == "__main__":                                                                                              # if code is in main.py (__main__) run following
    game = Game()                                                                                                       # initialize game() (class)
    game.run()                                                                                                          # run game (game-logic)