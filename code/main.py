######### IMPORT ##############

from settings import *
from pytmx.util_pygame import load_pygame
from player import *
from sprites import Sprite


######### CLASSes #############

class Game:
    def __init__(self):

        pygame.init()                                                                               # initialize pygame framework
        self.SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))                        # create screen with (x,y) (tuple)
        pygame.display.set_caption("School-Game-Project(11. Grade)")                                # set/change title (caption) of the window
        self.clock = pygame.time.Clock()                                                            # create a clock
        self.player = Player()                                                                      # create a player using Player() class
        
        # groups
        self.all_sprites = pygame.sprite.Group()                                                    # create a sprite group
        
        self.import_assets()                                                                        # import tilesets (assets)
        self.setup(self.tmx_maps['world'], 'spawn')                                                 # import this specific one tileset (mapset/asset)
        
    def import_assets(self):
        self.tmx_maps = {'world': load_pygame(os.path.join('..', 'data', 'maps', 'world.tmx'))}     # load world.tmx file (with given location of it)
        
    def setup(self, tmx_map, player_start_pos):
        for x,y, surf in tmx_map.get_layer_by_name('Terrain').tiles():                              # get only 'Terrain' layer from world.tmx
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)                          # parse information of sprite to Sprite() class
        
    def run(self):
        while True:
            dt = self.clock.tick() / 1000                                                           # tick every second  # dt = difference between previous and next frame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            self.SCREEN.fill((255, 255, 255))                                                       # fill SCREEN with white color and also refresh it
           
            userInput = pygame.key.get_pressed()                                                    # get user Input ( such as Keyboard Inputs/events)
            
            # DRAW MAP (tmx)
            for sprite in self.all_sprites:
                self.SCREEN.blit(sprite.image, (sprite.rect.x - self.player.camera_x, sprite.rect.y - self.player.camera_y)) 

            # DRAW OBJECTS:
            self.player.draw(self.SCREEN)                                                           # draw a Player on the Screen
            self.player.movement(userInput)                                                         # update player's position based on user input
            
            self.clock.tick(60)                                                                     # locking game-frames to 60fps
            pygame.display.update()                                                                 # update/refresh the screen




####### MAIN CODE ############

if __name__ == "__main__":                                                                          # if code is in main.py (__main__) run following
    game = Game()
    game.run()                                                                                      # run game (game-logic)
