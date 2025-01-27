######### IMPORT ##############

from settings import *

######### Variables ##############

loop = True                                                                                                             # loop variable

######### CLASSes ##############
class Button:
    def __init__(self,x,y,scale,image,hovered_image=None,pressed_image=None):
        self.image = image
        self.hovered_image = hovered_image if hovered_image else image
        self.pressed_image = pressed_image if pressed_image else image

        self.images = [self.image, self.hovered_image, self.pressed_image]
        self.scale = scale
        self.set_image(self.images[0], self.scale)

        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.pressed = False
        self.action = False

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def hovered(self):
        self.set_image(self.images[1], self.scale)

#    def pressed(self):
#        self.set_image(self.images[3], self.scale)

    def set_image(self, image, scale):
        width = image.get_width()
        height = image.get_height()
        scale = scale
        self.image = pygame.transform.scale(image, (int(width* scale),int(height* scale)))

    def draw(self, surface):
        self.action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.hovered()
            if pygame.mouse.get_just_pressed()[0] == 1 and self.pressed == False:
                self.pressed = True
                self.action = True
        else:
            self.set_image(self.images[0], self.scale)

        #DRAW BUTTON ON THE SCREEN
        surface.blit(self.image,(self.rect.x, self.rect.y))

 
