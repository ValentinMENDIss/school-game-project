from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("School-Game-Project(11. Grade)")
        self.clock = pygame.time.Clock()
        
    def run(self):
        while True:
            dt = self.clock.tick() / 1000 # tick every second  # lock to 60fps  # dt = difference between previous and next frame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.update()
            

if __name__ == "__main__":
    game = Game()
    game.run()