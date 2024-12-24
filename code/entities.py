######### IMPORT ##############

from settings import *

######### Sprites #############

PLAYER_IDLE = pygame.image.load(os.path.join('..', 'graphics', 'player_idle.png'))                                      # load sprite of the Player (in action: idle)

######### CLASSes ############

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)                                                                                        # this subclass sets up the basic properties and methods that it inherits from its parent class (group)
        self.image = PLAYER_IDLE.convert_alpha()                                                                        # assign image to the player # convert_alpha() function used to specify that the image should be rendered with alpha colors (for .png format).
        new_size_image = (self.image.get_width() * 4, self.image.get_height() * 4)                                      # declare new variable that has 4 times bigger scale than the player's image
        self.image = pygame.transform.scale(self.image, new_size_image)                                                 # scale the image by 4 times
        self.rect = self.image.get_frect(center=pos)                                                                    # convert image to rectangle (needed for collision in the future)

        self.direction = vector()                                                                                       # create a table(vector2d) which has direction input as a tuple

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector()  # by default (0,0) x and y
        if keys[pygame.K_UP]:
            input_vector.y -= 1
        if keys[pygame.K_DOWN]:
            input_vector.y += 1
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        self.direction = input_vector

    def move(self, dt):
        self.rect.center += self.direction * 250 * dt  # multiplying by dt = delta time (difference from last and next frame), so that our movement will be frame speed independent. It means it will not get faster or slower if fps changes.

    def update(self, dt):
        self.input()
        self.move(dt)