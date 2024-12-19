######### IMPORT ##############

from settings import *
from main import Game

######### Sprites #############

IDLE = pygame.image.load(os.path.join('..', 'graphics', 'player_idle.png'))   # Sprite of Dinosaur (in action: jumping)

######### CLASSes ############

class Player(Game):
    X_POS = 0                           # X-Coordinates of the player (at initialization)         
    Y_POS = 0                           # Y-Coordinates of the player (at initialization)

    def __init__(self):
        self.camera_x = CAMERA_X
        self.camera_y = CAMERA_Y

        self.image = IDLE
        new_size_image = (self.image.get_width() * 4, self.image.get_height() * 4)
        self.image = pygame.transform.scale(self.image, new_size_image)
        
        self.player_idle = True
        self.player_rect = self.image.get_rect()          # Convert image to rectangle (needed for collision (in the future...))
        self.player_rect.x = self.X_POS   
        self.player_rect.y = self.Y_POS        
        
    def movement(self, userInput):
        # linear movement
        if userInput [pygame.K_UP]:
            self.player_rect.y -= 5
        elif userInput [pygame.K_DOWN]:
            self.player_rect.y += 5
        elif userInput [pygame.K_LEFT]:
            self.player_rect.x -= 5
        elif userInput [pygame.K_RIGHT]:
            self.player_rect.x += 5

        # Update the camera position
        self.camera_x = self.player_rect.x - WINDOW_WIDTH // 2
        self.camera_y = self.player_rect.y - WINDOW_HEIGHT // 2
            
    def draw(self, SCREEN):                                     # draw function (def)
        SCREEN.blit(self.image, (self.player_rect.x - self.camera_x, self.player_rect.y - self.camera_y))
