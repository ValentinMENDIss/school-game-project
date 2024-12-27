from settings import *
   
#Loop Variable
loop = True 


START_IMG = pygame.image.load(os.path.join('..', 'graphics', 'button.png'))		                                        # Load images bild können wir selbst machen oder aus interent runterladen
EXIT_IMG = pygame.image.load(os.path.join('..', 'graphics', 'button.png'))		                                        # Load images


class Button():
    def __init__(self,x,y,image,scale):
        self.SCREEN = pygame.display.get_surface()                                                                      # initializing screen (SCREEN)
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width* scale),int(height* scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        
    def draw(self, surface):
        action = False 
        #get mouse position
        pos = pygame.mouse.get_pos()
        
        #check if mouse colide
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True 
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        #draw button on screen
        self.SCREEN.blit(self.image,(self.rect.x, self.rect.y))
        
        #return action
        print(action)
        
#start_button = Button(100,200,START_IMG, 0.8)		#create button instance
#exit_button = Button(100,500,EXIT_IMG, 0.8)			#create button instance
