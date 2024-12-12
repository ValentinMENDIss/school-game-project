# Player Code
from settings import *


IDLE = pygame.image.load(os.path.join("graphics", "dino_idle.png"))   # Sprite of Dinosaur (in action: jumping)

class Player:
    # Coordinates of the player
    X_POS = 0                        # X-Coordinates of the player (by initialization)         
    Y_POS = 0                      # Y-Coordinates of the player (by initialization)
    def __init__(self):
        self.image = IDLE
        self.player_idle = True
        self.player_rect = self.image.get_rect()          # Convert image to rectangle (needed for collision (in the future...))
        self.player_rect.x = self.X_POS   
        self.player_rect.y = self.Y_POS        
        
    def movement(self):
        if self.player_idle:
            pass
            
    def draw(self, SCREEN):                                     # draw function (def)
        SCREEN.blit(self.image, (self.X_POS, self.Y_POS))
