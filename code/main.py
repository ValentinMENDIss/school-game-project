######### IMPORT ##############

from settings import *
from pytmx.util_pygame import load_pygame
from player import *
from sprites import Sprite


######### CLASSes #############

class Game:
    def __init__(self):
        pygame.init()
        self.SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("School-Game-Project(11. Grade)")
        self.clock = pygame.time.Clock()                            # creating a clock
        self.player = Player()
        
        # groups
        self.all_sprites = pygame.sprite.Group()
        
        self.import_assets()
        self.setup(self.tmx_maps['world'], 'spawn')
        
    def import_assets(self):
        self.tmx_maps = {'world': load_pygame(os.path.join('..', 'data', 'maps', 'world.tmx'))}
        
    def setup(self, tmx_map, player_start_pos):
        for x,y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)
        
    def run(self):
        while True:
            dt = self.clock.tick() / 1000 # tick every second  # dt = difference between previous and next frame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            self.SCREEN.fill((255, 255, 255))                       # fill SCREEN with white color, also refresh it
           
            userInput = pygame.key.get_pressed()                # Gets user Inputs ( such as Keyboard Inputs/events)
            
            # DRAW MAP (tmx)
            self.all_sprites.draw(self.SCREEN)                  
           
            # DRAW OBJECTS:
            self.player.draw(self.SCREEN)                                 # Draw a Player on the Screen
            self.player.movement(userInput)     
            
            self.clock.tick(60)                      # locking game-frames to 60fps
            pygame.display.update()         




####### MAIN CODE ############

if __name__ == "__main__":
    game = Game()
    game.run()
