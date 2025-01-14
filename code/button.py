######### IMPORT ##############

from settings import *

######### Variables ##############

loop = True                                                                                                             # loop variable

# LOADING IMAGES
START_IMG = pygame.image.load(os.path.join('..', 'graphics', 'start-button.png'))		                                # load image for start button
EXIT_IMG = pygame.image.load(os.path.join('..', 'graphics', 'exit-button.png'))		                                    # load image for exit button
RETURN_IMG = pygame.image.load(os.path.join('..', 'graphics', 'return-button.png'))		                                # load image for return button
SETTINGS_IMG = pygame.image.load(os.path.join('..', 'graphics', 'settings-button.png'))		                                # load image for settings button
TEST_IMG = pygame.image.load(os.path.join('..', 'graphics', 'test-button.png'))

######### CLASSes ##############
class Button:
    def __init__(self,x,y,image,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width* scale),int(height* scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.clicked = False
        self.action = False
        self.prev_left_button_state = False

    def draw(self, surface):
        self.action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_just_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.action = True
            if pygame.mouse.get_just_pressed()[0] == 1 and self.clicked ==  0:
                self.clicked = False            

        #DRAW BUTTON ON THE SCREEN
        surface.blit(self.image,(self.rect.x, self.rect.y))

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def get_action(self):
        return self.action
