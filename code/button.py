from settings import *
   
#Loop Variable
loop = True 


start_img = pygame.image.load('start_btn.png').convert_alpha()		#Load images bild können wir selbst machen oder aus interent runterladen
exit_img = pygame.image.load('exit_btn.png').convert_alpha()		#Load images


class Button():
    def __init__(self,x,y,image,scale):
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
        screen.blit(self.image,(self.rect.x, self.rect.y))
        
        return action
        
start_button = Button(100,200,start_img, 0.8)		#create button instance
exit_button = Button(100,500,exit_img, 0.8)			#create button instance
