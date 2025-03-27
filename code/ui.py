######### IMPORT ##############

import settings

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

        self.hovered_on = False                                                                                             # variable that stores bool value to show whether the button is being hovered on or not

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
        self.image = settings.pygame.transform.scale(image, (int(width* scale),int(height* scale)))

    def draw(self, surface):
        self.action = False
        pos = settings.pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.hovered()
            if settings.pygame.mouse.get_just_pressed()[0] == 1 and self.pressed == False:
                self.pressed = True
                self.action = True
        else:
            self.set_image(self.images[0], self.scale)

        #DRAW BUTTON ON THE SCREEN
        surface.blit(self.image,(self.rect.x, self.rect.y))

class Slider():
    def __init__(self, x, y, width, height, min_value, max_value, initial_value, centered=False, show_value=True):
        self.x = x                                                                                  # position on x-axis of slider
        self.y = y                                                                                  # position on y-axis of slider
        self.width = width                                                                          # width of slider
        self.height = height                                                                        # height of slider
        self.rect = settings.pygame.Rect(self.x, self.y, self.width, self.height)                            # create rectangle
        if centered:                                                                                
            self.rect.center = (self.x, self.y)                                                     # center slider (set rectangle anchor in the middle/center of rectangle)
        self.min_value = min_value                                                                  # minimal allowed value
        self.max_value = max_value                                                                  # maximum allowed value
        self.value = initial_value                                                                  # value given when initialized
        self.show_value = show_value
        self.handle_x = self.rect.x + int(self.value * self.width)
        self.handle_y = self.rect.y + self.height // 2
        self.handle_radius = self.height // 1.50
        self.is_dragging = False                                                                    # declaring variable that holds bool value for dragging of the slider

    # CHECK USER'S INPUT
    def checkForInput(self, mouse_pos, pressed_button):                                
        self.mouse_pos = mouse_pos                                                                  # declare new variable that holds mouse position in a tuple
        if self.rect.collidepoint(self.mouse_pos):
            if pressed_button == 1:                                                                 # check whether left mouse button has been pressed
                self.is_dragging = True                                                                                 # assign True (bool) to variable is_dragging
        else:
            self.is_dragging = False                                                                            

        if self.is_dragging:                                                                                            # if user is dragging slider, do following:
            self.value = ((self.mouse_pos[0] - self.rect.x) / self.width)                                 # Define the rectangle
            self.value = max(0, min(1, self.value))
            self.value = float(f"{self.value:.2f}")
            self.handle_x = self.rect.x + int(self.value * self.width)
            self.handle_y = self.rect.y + self.height // 2
 
    def draw(self, surface):
        if self.show_value:
            self.valuetext = settings.SMALLTEXT.render(str(self.value), True, (0, 0, 0)).convert_alpha()
            self.valuetextrect = self.valuetext.get_rect()
            self.valuetextrect.center = (self.x, self.y - 50)
            surface.blit(self.valuetext, self.valuetextrect)

        settings.pygame.draw.rect(surface, (255, 255, 255), self.rect)
        settings.pygame.draw.rect(surface, (186, 186, 186), (self.rect.x + (self.handle_x - self.rect.x), self.rect.y, self.width - int(self.value * self.width), self.height))

        settings.pygame.draw.circle(surface, (0, 0, 0), (self.handle_x, self.handle_y), self.handle_radius)

class InputBox:
    def __init__(self, x, y, width, height, initial_value, input_type=int, centered=False):
        self.x = x                                                                                  # position on x-axis of slider
        self.y = y                                                                                  # position on y-axis of slider
        self.width = width                                                                          # width of slider
        self.height = height                                                                        # height of slider
        self.rect = settings.pygame.Rect(self.x, self.y, self.width, self.height)                            # create rectangle
        if centered:
            self.rect.center = (self.x, self.y)                                                     # center slider (set rectangle anchor in the middle/center of rectangle)
        self.value = str(initial_value)
        self.input_type = input_type
        self.pressed = False
        
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.pressed = True
            return True
        self.pressed = False
        return False
    
    def update_value(self, event):
        new_value = event.unicode
        if self.input_type == int:
            if new_value.isdigit():
                self.value += new_value
        if new_value == "\x08":                                                                     # if BACKSPACE is clicked: remove last digit/character
            self.value = self.value[:-1]
        if len(self.value) > 0:
            if new_value == "\r":                                                               # if ENTER is clicked: return value
                if self.input_type == int:
                    return int(self.value)
                else:
                    return self.value
                
    def draw(self, surface):
        if self.pressed == False:
            settings.pygame.draw.rect(surface, (255, 255, 255), self.rect) # white colour
        else:
            settings.pygame.draw.rect(surface, (250, 250, 250), self.rect) # snow colour
        self.valuetext = settings.SMALLTEXT.render(str(self.value), True, (0, 0, 0)).convert_alpha()
        self.valuetextrect = self.valuetext.get_rect()
        self.valuetextrect.center = (self.x, self.y)
        surface.blit(self.valuetext, self.valuetextrect)


        