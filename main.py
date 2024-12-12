######### IMPORT ##############

from settings import *
from player import *


######### CLASSes #############

class Game:
    def __init__(self):
        pygame.init()
        self.SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("School-Game-Project(11. Grade)")
        self.clock = pygame.time.Clock()                            # creating a clock
        self.player = Player()
        
    def run(self):
        while True:
            dt = self.clock.tick() / 1000 # tick every second  # dt = difference between previous and next frame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            self.SCREEN.fill((255, 255, 255))                       # fill SCREEN with white color, also refresh it
           
            userInput = pygame.key.get_pressed()                # Gets user Inputs ( such as Keyboard Inputs/events)
           
            # DRAW OBJECTS:
            self.player.draw(self.SCREEN)                                 # Draw a Player on the Screen
            self.player.movement(userInput)     
            
            self.clock.tick(60)                      # locking game-frames to 60fps
            pygame.display.update()         




####### MAIN CODE ############

if __name__ == "__main__":
    game = Game()
    game.run()
