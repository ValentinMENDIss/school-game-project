from settings import *
   
#Loop Variable
loop = True

# Loading Images
START_IMG = pygame.image.load(os.path.join('..', 'graphics', 'start-button.png'))		                                        # Load images bild können wir selbst machen oder aus interent runterladen
EXIT_IMG = pygame.image.load(os.path.join('..', 'graphics', 'start-button.png'))		                                        # Load images


class Button():
    def __init__(self,x,y,image,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width* scale),int(height* scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.clicked = False
        
    def draw(self, surface):
        self.action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        
        #check if mouse collides
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True 
                self.action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        #draw button on screen
        surface.blit(self.image,(self.rect.x, self.rect.y))

    def get_action(self):
        return self.action