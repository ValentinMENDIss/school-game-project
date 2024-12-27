######### IMPORT ##############
from settings import *
from pytmx.util_pygame import load_pygame
from entities import *
from sprites import Sprite
from groups import *
from dialog import *

######### CLASSES #############

class Game:
    def __init__(self):
        # INITIALIZE FRAMEWORK
        pygame.init()                                                                                                   # initialize pygame framework
        pygame.font.init()                                                                                              # initialize pygame text/font framework

        # INITIALIZE VARIABLES
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
        self.setup(self.tmx_maps['world'], 'spawn')                                                       # import this specific one tileset (mapset/asset)
        
    def import_assets(self):
        self.tmx_maps = {'world': load_pygame(os.path.join('..', 'data', 'maps', 'world.tmx'))}                         # load world.tmx file (with given location of it)
        
    def setup(self, tmx_map, player_start_pos):
        for x,y, surf in tmx_map.get_layer_by_name('Terrain').tiles():                                                  # get only 'Terrain' layer from world.tmx
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)                                         # parse information of sprite to Sprite() class

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player' and obj.properties['pos'] == player_start_pos:                                      # check whether the object's name is Player and its properties for pos(position). Check also whether it is the same as player_start_pos
                self.player = Player((obj.x, obj.y), self.all_sprites)                                             # create player() instance with object's x and y coordinates that we got from tilemap(tmx). And assign player() instance to AllSprites() group/class
            if obj.name == 'Character' and obj.properties['pos'] == 'bottom-right':
                self.npc = NPC((obj.x, obj.y), self.all_sprites)

    # DIALOG SYSTEM
    def input(self):
        keys = pygame.key.get_just_pressed()                                                                            # initialize new varable(keys) that will get user's input, but the buttons can be detected as pressed and not as hold too.
        if keys[pygame.K_e]:                                                                                            # if just pressed key is e do following:
            if abs(self.npc.rect[0] - self.player.rect[0]) <= 200 and abs(self.npc.rect[1] - self.player.rect[1]) <= 200: # check npc's and player's position. If the differences between each x and y coordinates are smaller in value than 200 do following:
                self.interact = True                                                                                    # assign following value to self.interact variable: True


    def run(self):
        # PYGAME EVENTS
        while True:
            dt = self.clock.tick() / 1000                                                                               # tick every second  # dt = difference between previous and next frame
            for event in pygame.event.get():                                                                            # for every single event that is available in pygame do following:
                if event.type == pygame.QUIT:                                                                           # if event type is 'QUIT' do following:
                    pygame.quit()                                                                                       # quit/exit

            # PYGAME LOGIC
            self.all_sprites.update(dt)                                                                                 # update screen (all sprites) by FPS
            self.SCREEN.fill('white')                                                                                   # fill screen with white color, so it's fully updated
            self.all_sprites.draw(self.player.rect.center)                                                              # draw all sprites to the center of the rectangle of the player (camera)
            self.input()                                                                                                # take user's input

            if self.interact == True:                                                                                   # check whether interact condition is true or not (bool check)
                self.npc.interact("OMG, I CAN SPEAK!!! Thank you developers :3", self.player.rect)                 # interact with npc, text in speech bubble
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
