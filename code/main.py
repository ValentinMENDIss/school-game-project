######### IMPORT ##############
from settings import *
from pytmx.util_pygame import load_pygame
from entities import *
from sprites import Sprite
from groups import *

######### CLASSes #############

class Game:
    def __init__(self):

        pygame.init()                                                                               # initialize pygame framework
        pygame.font.init()
        self.SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))                        # create screen with (x,y) (tuple)
        pygame.display.set_caption("School-Game-Project(11. Grade)")                                # set/change title (caption) of the window
        self.clock = pygame.time.Clock()                                                            # create a clock

        # GROUPS
        self.all_sprites = AllSprites()                                                    # create a sprite group # assigns to AllSprites() Class
        
        self.import_assets()                                                                        # import tilesets (assets)
        self.setup(self.tmx_maps['world'], 'spawn')                                   # import this specific one tileset (mapset/asset)
        
    def import_assets(self):
        self.tmx_maps = {'world': load_pygame(os.path.join('..', 'data', 'maps', 'world.tmx'))}     # load world.tmx file (with given location of it)
        
    def setup(self, tmx_map, player_start_pos):
        for x,y, surf in tmx_map.get_layer_by_name('Terrain').tiles():                              # get only 'Terrain' layer from world.tmx
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)                     # parse information of sprite to Sprite() class

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player' and obj.properties['pos'] == player_start_pos:
                self.player = Player((obj.x, obj.y), self.all_sprites)
            if obj.name == 'Character' and obj.properties['pos'] == 'bottom-right':
                self.npc = NPC((obj.x, obj.y), self.all_sprites)

    def run(self):
        while True:
            dt = self.clock.tick() / 1000                                                           # tick every second  # dt = difference between previous and next frame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # pygame logic
            self.all_sprites.update(dt)                                                                                 # update screen (all sprites) by FPS
            self.SCREEN.fill('white')                                                                                   # fill screen with white color, so it's fully updated
            self.all_sprites.draw(self.player.rect.center)                                                              # draw all sprites to the center of the rectangle of the player (camera)




            smallText = pygame.font.Font(os.path.join('..','font', 'Pixeltype.ttf'), 20)                                                                          # Set Font and Size for the Small Text

            # SMALL TEXT

            smallText = smallText.render("Made as a school project, Have fun :) (TEST FRAMEWORK: TEXT)", True,
                                         (0, 0, 0)).convert_alpha()  # Render a Small Text
            smallTextRect = smallText.get_rect()  # Get a Rectangle of the small Text ( needed, to be able to place the Text precisely )
            smallTextRect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30)  # Place a Text in the Center of the screen ( X-Coordinates ) and Bottom of the screen ( Y-Coordinates )
            self.SCREEN.blit(smallText, smallTextRect)  # Draw a Text on the Screen

            pygame.display.update()                                                                                     # refresh(update) the screen

####### MAIN CODE ############

if __name__ == "__main__":                                                                          # if code is in main.py (__main__) run following
    game = Game()
    game.run()                                                                                      # run game (game-logic)
