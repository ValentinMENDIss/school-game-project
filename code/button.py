######### IMPORT ##############

from settings import *

######### Variables ##############

loop = True                                                                                                             # loop variable

# LOADING IMAGES
START_IMG = pygame.image.load(os.path.join('..', 'graphics', 'start-button.png'))		                                # load image for start button
EXIT_IMG = pygame.image.load(os.path.join('..', 'graphics', 'exit-button.png'))		                                    # load image for exit button
RETURN_IMG = pygame.image.load(os.path.join('..', 'graphics', 'return-button.png'))		                                # load image for return button
SETTINGS_IMG = pygame.image.load(os.path.join('..', 'graphics', 'settings-button.png'))		                                # load image for settings button

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
        
    def draw(self, surface):
        self.action = False
        pos = pygame.mouse.get_pos()                                                                                    # get mouse position


        if self.rect.collidepoint(pos):                                                                                 # check if mouse collides with the button
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True 
                self.action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #DRAW BUTTON ON THE SCREEN
        surface.blit(self.image,(self.rect.x, self.rect.y))
    def get_action(self):
        return self.action